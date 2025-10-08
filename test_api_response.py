#!/usr/bin/env python3
import requests
import json
import re

def test_api_response():
    # Test with real TLDR AI URL using GET method with query parameters
    base_url = "http://localhost:8000/api/v1/tldr"
    target_url = "https://tldr.tech/ai/2025-10-07"
    
    # Construct URL with query parameters
    tldr_url = f"{base_url}?url={target_url}&force_refresh=true"
    
    print("Testing with real TLDR AI page...")
    print(f"URL: {tldr_url}")
    print("-" * 50)
    
    try:
        response = requests.get(tldr_url)
        response.raise_for_status()
        
        data = response.json()
        
        print(f"Success: {data.get('success', False)}")
        print(f"Processing time: {data.get('processing_time', 'N/A')} seconds")
        print("-" * 50)
            
        if 'data' in data:
            article_data = data['data']
            print(f"AI Processed: {article_data.get('ai_processed', False)}")
            print(f"Title: {article_data.get('title', 'N/A')}")
            print(f"URL: {article_data.get('url', 'N/A')}")
            print("-" * 50)
            
            # Check for sections data
            if 'sections' in article_data:
                sections = article_data['sections']
                print(f"Sections found: {len(sections)}")
                for i, section in enumerate(sections):
                    print(f"  Section {i+1}: {section.get('title', 'No title')} - {len(section.get('content', ''))} chars")
                    articles = section.get('articles', [])
                    print(f"    Articles: {len(articles)}")
                    for j, article in enumerate(articles[:2]):  # 只显示前2个文章
                        print(f"      Article {j+1}: {article.get('title', 'No title')[:50]}...")
                        links = article.get('links', [])
                        print(f"        Links: {len(links)}")
                        if links:
                            print(f"        First link: {links[0]}")
            else:
                print("No sections data found")
                print(f"Available keys in article_data: {list(article_data.keys())}")
            print("-" * 50)
            
            # Extract and display references
            references = article_data.get('references', [])
            print(f"References ({len(references)}):")
            for i, ref in enumerate(references, 1):
                if isinstance(ref, dict):
                    print(f"  [{i}] Title: {ref.get('title', 'No title')}")
                    print(f"      Content: {ref.get('content', 'No content')[:100]}...")
                    print(f"      Section: {ref.get('section', 'No section')}")
                    print(f"      URL: {ref.get('url', 'No URL')}")
                    print(f"      Index: {ref.get('index', 'No index')}")
                    print("      ---")
                else:
                    print(f"  [{i}] {ref}")
            
            # Check for citation markers in summary
            summary = article_data.get('summary', '')
            if summary:
                citation_markers = re.findall(r'\[(\d+)\]', summary)
                print(f"Citation markers found in summary: {citation_markers}")
                print("-" * 30)
                print("Summary preview:")
                print(summary[:500] + "..." if len(summary) > 500 else summary)
                        
        else:
            print("No 'data' field in response")
            print(f"Response keys: {list(data.keys())}")
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    test_api_response()