import charms.reactive as reactive
import charms.reactive.flags as flags
import charmhelpers.core.hookenv as hookenv


class MungeAuthProvides(reactive.Endpoint):
    def expose_munge_key(self, munge_key):
        self._exposed_munge_key = munge_key
        hookenv.log('expose_munge_key(): exposed in MungeAuthProvides')

    
    @reactive.when('endpoint.{endpoint_name}.changed')
    @reactive.when('munge.exposed')
    def provide_munge_key(self):
        '''Provide an exposed munge key. Changed flag is set
        when new units are joined as the relation lifecycle
        includes a joined and consecutive changed event'''
        for rel in self.relations:
            rel.to_publish.update({'munge_key': self._exposed_munge_key})
        flags.clear_flag(self.expand_name(
            'endpoint.{endpoint_name}.changed'))
        hookenv.log('provide_munge_key(): munge key published on endpoint in MungeAuthProvides')
