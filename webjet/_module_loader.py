
class MultiModuleLoader(object):
    """
    Loads modules in order of their priority specified
    by the `PRIORITY' field and their dependencies specified
    by the `DEPENDENCIES' field
    """

    def __init__(self, modules=[]):
        self._loaded = []
        self._modules = modules

        self._load_order = []

    def _load_module(self, module, deps, action, params, resolv=True):
        if action == 'run':
            print('Running', module.__name__)

        if module in self._loaded:
            print('Loaded multiple times:', module.__name__)
            return

        # Append the modules to the list with the
        # loaded modules.
        self._loaded.append(module)

        if resolv:
            print('Resolving dependencies of', module.__name__)

            # Check whether the dependencies were
            # already resolved. Otherwise resolve them.
            deps.sort(key=self._cmp_modules)
            self._load(deps, action, params, resolv)
            self._load_order.append(module)

        # Execute the specified action on the module.
        module.__dict__[action](*params)

    def _load(self, modules, action, params, resolv=True):
        for mod in modules:
            # Load the module's dependencies and the module itself.
            deps = mod.DEPENDENCIES if 'DEPENDENCIES' in mod.__dict__ else []

            self._load_module(mod, deps, action, params, resolv)

    def load(self, action, params=[]):
        """
        Loads all added modules and executes the
        specified ``action'' (A string describing the method to call).
        """

        self._loaded = []

        if self._load_order:
            self._load(self._load_order, action, params, False)
        else:
            self._load(self._modules, action, params)

    def add(self, module):
        """
        Add the ``module'' to the module list.
        """

        if module in self._modules:
            print('Added multiple times:', module.__name__)
            return

        self._modules.append(module)
        self._modules.sort(key=self._cmp_modules)

        self._load_order = []

    def _cmp_modules(self, x):
        return x.PRIORITY
