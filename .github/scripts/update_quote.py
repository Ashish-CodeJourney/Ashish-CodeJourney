import requests
import random
import re
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_programming_quote():
    # List of APIs we can try
    apis = [
        {
            "url": "https://programming-quotes-api.herokuapp.com/quotes/random",
            "extract": lambda r: f'"{r["en"]}" - {r["author"]}'
        },
        {
            "url": "https://quotes.stormconsultancy.co.uk/random.json",
            "extract": lambda r: f'"{r["quote"]}" - {r["author"]}'
        },
        {
            "url": "https://api.quotable.io/random?tags=technology,programming",
            "extract": lambda r: f'"{r["content"]}" - {r["author"]}'
        }
    ]
    
    # Try each API until we get a successful response
    for api in apis:
        try:
            logger.info(f"Trying to fetch quote from: {api['url']}")
            response = requests.get(api["url"], timeout=10)  # Added timeout
            response.raise_for_status()  # Will raise an exception for 400/500 status codes
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Successfully fetched quote from {api['url']}")
                logger.info(f"Response data: {data}")
                return api["extract"](data)
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching from {api['url']}: {str(e)}")
        except (KeyError, ValueError) as e:
            logger.error(f"Error parsing response from {api['url']}: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error with {api['url']}: {str(e)}")
    
    logger.warning("All APIs failed, using fallback quotes")
    # Fallback quotes if APIs fail
    fallback_quotes = [
        '"Code is like humor. When you have to explain it, it\'s bad." - Cory House',
        '"First, solve the problem. Then, write the code." - John Johnson',
        '"Make it work, make it right, make it fast." - Kent Beck',
        '"Clean code always looks like it was written by someone who cares." - Michael Feathers',
        '"Programming isn\'t about what you know; it\'s about what you can figure out." - Chris Pine',
        '"The only way to learn a new programming language is by writing programs in it." - Dennis Ritchie',
        '"The best error message is the one that never shows up." - Thomas Fuchs',
        '"The most important property of a program is whether it accomplishes the intention of its user." - C.A.R. Hoare',
        '"Simplicity is prerequisite for reliability." - Edsger W. Dijkstra',
        '"Code never lies, comments sometimes do." - Ron Jeffries'
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
// Updated every 12 hours
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
