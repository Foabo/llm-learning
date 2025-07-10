import os
from jinja2 import Environment,FileSystemLoader

def apply_prompt_template(prompt_template:str,**kwargs)->str:
    """
    Apply a prompt template to a set of keyword arguments.
    Args:
        prompt_template: The prompt template to apply.
        **kwargs: The keyword arguments to apply to the prompt template.
    Returns:
        The prompt template with the keyword arguments applied.
    """
    template_dir=os.path.join(os.path.dirname(__file__),"templates")
    env=Environment(loader=FileSystemLoader(template_dir))
    template=env.get_template(f"{prompt_template}.jinja-md")
    return template.render(**kwargs)

if __name__ == "__main__":
    print(apply_prompt_template("planner"))