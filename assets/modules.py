import os


def load_modules(dp):
    txt = 0
    for filename in os.listdir('modules'):
        if filename.endswith(".py") and filename != "__init__.py" and not filename.startswith("add"):
            module_name = filename[:-3]
            module = __import__(f"modules.{module_name}", fromlist=["register_handlers"])
            module.register_handlers(dp)
            txt += 1
    if txt > 0:
        print(f'Импортировано {txt} модулей.')