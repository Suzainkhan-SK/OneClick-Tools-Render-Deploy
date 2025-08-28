import requests
import json
import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

def test_all_models():
    """Test all image generation models"""
    a4f_api_key = os.environ.get('A4F_API_KEY')
    if not a4f_api_key:
        print("ERROR: A4F_API_KEY environment variable is not set!")
        return
    
    # Test models you want to use
    test_models = [
        'provider-4/imagen-3',
        'provider-4/imagen-4',
        'provider-6/sana-1.5-flash',
        'provider-1/FLUX.1-schnell',
        'provider-6/sana-1.5',
        'provider-6/qwen-image',
        'provider-3/FLUX.1-dev',
        'provider-2/FLUX.1-schnell-v2'
    ]
    
    results = []
    test_prompt = "A cute baby sea otter"
    
    for model in test_models:
        try:
            # Get model configuration
            model_config = get_model_config(model)
            if not model_config:
                results.append({"model": model, "status": "error", "message": "No config found"})
                continue
            
            # Prepare request
            payload = {
                "model": model,
                "prompt": test_prompt,
                "n": 1,
                "size": model_config['supported_sizes'][0]
            }
            
            # Add model-specific parameters
            if model_config.get('default_params'):
                payload.update(model_config['default_params'])
            
            # FLUX models might need special prompt formatting
            if 'flux' in model.lower():
                payload['prompt'] = enhance_flux_prompt(test_prompt)
            
            # Make API call
            a4f_url = "https://api.a4f.co/v1/images/generations"
            headers = {
                "Authorization": f"Bearer {a4f_api_key}",
                "Content-Type": "application/json"
            }
            
            print(f"Testing model: {model}")
            response = requests.post(a4f_url, headers=headers, data=json.dumps(payload), timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                image_urls = parse_model_response(data, model)
                results.append({
                    "model": model, 
                    "status": "success", 
                    "code": response.status_code,
                    "image_count": len(image_urls) if image_urls else 0
                })
            else:
                results.append({
                    "model": model, 
                    "status": "error", 
                    "code": response.status_code,
                    "message": response.text[:200]  # First 200 chars of error
                })
                
        except Exception as e:
            results.append({"model": model, "status": "error", "message": str(e)})
    
    # Print results
    print("\n" + "="*60)
    print("MODEL TEST RESULTS")
    print("="*60)
    
    for result in results:
        status_icon = "✅" if result['status'] == 'success' else "❌"
        print(f"{status_icon} {result['model']}: {result['status']}")
        if result['status'] == 'success':
            print(f"   Images generated: {result.get('image_count', 0)}")
        else:
            print(f"   Error: {result.get('message', 'Unknown error')}")
        print()

def get_model_config(model):
    """Get configuration for specific models"""
    configs = {
        'provider-4/imagen-3': {
            'max_images': 4,
            'supported_sizes': ['1024x1024', '1152x896', '896x1152'],
            'default_params': {}
        },
        'provider-4/imagen-4': {
            'max_images': 4,
            'supported_sizes': ['1024x1024', '1152x896', '896x1152', '1216x832', '832x1216'],
            'default_params': {}
        },
        'provider-6/sana-1.5-flash': {
            'max_images': 4,
            'supported_sizes': ['1024x1024', '1152x896', '896x1152'],
            'default_params': {}
        },
        'provider-1/FLUX.1-schnell': {
            'max_images': 4,
            'supported_sizes': ['1024x1024', '512x512', '768x768'],
            'default_params': {'guidance_scale': 5.0, 'num_inference_steps': 25}
        },
        'provider-6/sana-1.5': {
            'max_images': 4,
            'supported_sizes': ['1024x1024', '1152x896', '896x1152'],
            'default_params': {}
        },
        'provider-6/qwen-image': {
            'max_images': 4,
            'supported_sizes': ['1024x1024', '1152x896', '896x1152'],
            'default_params': {}
        },
        'provider-3/FLUX.1-dev': {
            'max_images': 2,
            'supported_sizes': ['1024x1024', '1152x896', '896x1152', '1344x768', '768x1344'],
            'default_params': {'guidance_scale': 7.5, 'num_inference_steps': 50}
        },
        'provider-2/FLUX.1-schnell-v2': {
            'max_images': 4,
            'supported_sizes': ['1024x1024', '512x512', '768x768'],
            'default_params': {'guidance_scale': 5.0, 'num_inference_steps': 25}
        }
    }
    return configs.get(model)

def enhance_flux_prompt(prompt):
    """Enhance prompts for FLUX models"""
    if len(prompt.split()) < 10:
        return f"{prompt}, highly detailed, professional quality, sharp focus"
    return prompt

def parse_model_response(response_data, model):
    """Parse API response to extract image URLs"""
    if response_data and 'data' in response_data and isinstance(response_data['data'], list):
        return [item['url'] for item in response_data['data'] if 'url' in item]
    
    if 'images' in response_data and isinstance(response_data['images'], list):
        return response_data['images']
    
    if 'urls' in response_data and isinstance(response_data['urls'], list):
        return response_data['urls']
    
    return []

if __name__ == '__main__':
    test_all_models()