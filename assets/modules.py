import install
import os

MODULES = {}


def load_modules(dp):
    txt = 0
    mlist = []
    for filename in os.listdir('modules'):
        if filename.endswith(".py") and filename != "__init__.py" and not filename.startswith("add"):
            fmodule_name = filename[:-3]
            module = __import__(f"modules.{fmodule_name}", fromlist=["register_handlers"])
            module.register_handlers(dp)
            txt += 1

            if hasattr(module, 'MODULE_DESCRIPTION'):
                module_info = module.MODULE_DESCRIPTION
                module_name = module_info.get('name', 'Без названия')
                module_description = module_info.get('description', 'Нет описания')
                mlist.append(module_name)
                MODULES[fmodule_name] = {'name': module_name, 'description': module_description}
            
    if txt > 0:
        mlist = ', '.join(mlist)
        print(f'Загрузка модулей "{mlist}"')
        print(f'Импортировано {txt} модулей.')
        

def load_new_mod(filename, dp):
    if filename.endswith(".py") and filename != "__init__.py" and not filename.startswith("add"):
        fmodule_name = filename[:-3]
        module = __import__(f"modules.{fmodule_name}", fromlist=["register_handlers"])
        module.register_handlers(dp)

        if hasattr(module, 'MODULE_DESCRIPTION'):
            module_info = module.MODULE_DESCRIPTION
            module_name = module_info.get('name', 'Без названия')
            module_description = module_info.get('description', 'Нет описания')
            MODULES[fmodule_name] = {'name': module_name, 'description': module_description}