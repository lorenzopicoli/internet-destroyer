# The python script that litters the internet for pennies

Python script that litters the internet by generating thousands of wordpress articles and uploads them

Env vars required:

```
OPENAI_API_KEY
WORDPRESS_API_KEY
```

Example usage:

```
python3 src/cli.py  --prompt "Mechanical keyboards" --blog-url "aaa.com" --author bbbb --keyword-count 10 --idea-count 2  --section-count 3
```
