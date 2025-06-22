#prompt_manager.py

from pathlib import Path
import frontmatter
from jinja2 import Environment, FileSystemLoader, StrictUndefined, TemplateError, meta



class PromptManager:
    _env = None

    @classmethod

    def _get_env(cls, prompt_cat: str, ):
        template_dir: str = Path(__file__).parent / prompt_cat
        if cls._env is None:
            cls._env = Environment(
                loader=FileSystemLoader(template_dir),
                undefined=StrictUndefined
                ) 
            
        return cls._env


    @staticmethod
    def get_prompt( prompt_cat, prompt_name: str, **kwargs):
        env = PromptManager._get_env(prompt_cat)
        template_path = f"{prompt_name}.j2"
        print(env.loader.get_source(env, template_path))
        with open(env.loader.get_source(env, template_path)[1]) as file:
            post = frontmatter.load(file)   
        template = env.from_string(post.content)

        try:
            return template.render(**kwargs)
        except TemplateError as e:
            raise TemplateError(f"Error rendering template {template_path}: {e}")
        
    @staticmethod
    def get_template_info(template):
        env = PromptManager._get_env()
        template_path = f"{template}.j2"
        with open(env.loader.get_source(env, template_path)[1]) as file:
            post = frontmatter.load(file)
        return post.metadata
    
    @staticmethod
    def get_template_variables(template):
        env = PromptManager._get_env()
        template_path = f"{template}.j2"
        with open(env.loader.get_source(env, template_path)[1]) as file:
            post = frontmatter.load(file)
        
        ast = env.parse(post.content)
        variables = meta.find_undeclared_variables(ast)

        return {
            "name": template,
            "description": post.metadata.get("description", ""),
            "author": post.metadata.get("author", ""),
            "variables": list(variables), 
            "frontmatter": post.metadata,
        }    
        
        
        
        
    