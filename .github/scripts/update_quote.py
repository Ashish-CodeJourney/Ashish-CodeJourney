import requests
import random
import re
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_programming_quote():
    # Updated list of APIs with more reliable endpoints
    apis = [
        {
            "url": "https://zenquotes.io/api/random",
            "extract": lambda r: f'"{r[0]["q"]}" - {r[0]["a"]}'
        },
        {
            "url": "https://api.github.com/zen",
            "extract": lambda r: f'"{r}"'
        },
        {
            "url": "https://api.quotable.io/random?tags=technology",
            "extract": lambda r: f'"{r["content"]}" - {r["author"]}',
            "verify": False  # Disable SSL verification for this API
        }
    ]
    
    # Try each API until we get a successful response
    for api in apis:
        try:
            logger.info(f"Trying to fetch quote from: {api['url']}")
            verify_ssl = api.get("verify", True)
            response = requests.get(api["url"], timeout=10, verify=verify_ssl)
            response.raise_for_status()
            
            if response.status_code == 200:
                if api["url"] == "https://api.github.com/zen":
                    data = response.text
                else:
                    data = response.json()
                logger.info(f"Successfully fetched quote from {api['url']}")
                return api["extract"](data)
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching from {api['url']}: {str(e)}")
        except (KeyError, ValueError) as e:
            logger.error(f"Error parsing response from {api['url']}: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error with {api['url']}: {str(e)}")
    
    logger.warning("All APIs failed, using fallback quotes")
    # Enhanced fallback quotes with more programming-specific content
    fallback_quotes = [
        '"Any fool can write code that a computer can understand. Good programmers write code that humans can understand." - Martin Fowler',
        '"Perfection is achieved not when there is nothing more to add, but rather when there is nothing more to take away." - Antoine de Saint-Exupery',
        '"Code is like poetry; it\'s not just about making it work, it\'s about making it elegant." - Unknown',
        '"The function of good software is to make the complex appear to be simple." - Grady Booch',
        '"Before software can be reusable it first has to be usable." - Ralph Johnson',
        '"Simplicity is the soul of efficiency." - Austin Freeman',
        '"Every great developer you know got there by solving problems they were unqualified to solve until they actually did it." - Patrick McKenzie',
        '"The best way to predict the future is to implement it." - David Heinemeier Hansson',
        '"Good code is its own best documentation." - Steve McConnell',
        '"Software is a great combination of artistry and engineering." - Bill Gates',
        '"The only way to go fast is to go well." - Robert C. Martin',
        '"Clean code always looks like it was written by someone who cares." - Michael Feathers',
        '"Code never lies, comments sometimes do." - Ron Jeffries',
        '"A primary cause of complexity is that software vendors uncritically adopt almost any feature that users want." - Niklaus Wirth',
        '"Programming is the art of telling another human what one wants the computer to do." - Donald Knuth'
    ]
    return random.choice(fallback_quotes)

def update_readme():
    try:
        with open("README.md", "r", encoding="utf-8") as file:
            content = file.read()
        
        quote = get_programming_quote()
        logger.info(f"Generated quote: {quote}")
        
        formatted_quote = f'''<!--QUOTE:start-->
```javascript
{quote}
```
<!--QUOTE:end-->'''
        
        # Replace the quote section
        pattern = r"<!--QUOTE:start-->.*?<!--QUOTE:end-->"
        new_content = re.sub(pattern, formatted_quote, content, flags=re.DOTALL)
        
        with open("README.md", "w", encoding="utf-8") as file:
            file.write(new_content)
            
        logger.info("Successfully updated README.md")
            
    except Exception as e:
        logger.error(f"Error updating README: {str(e)}")
        raise

if __name__ == "__main__":
    update_readme()
