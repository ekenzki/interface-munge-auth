import charms.reactive as reactive
import charms.reactive.flags as flags
import charmhelpers.core.hookenv as hookenv
import charms.leadership as leadership


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
        hookenv.log('provide_munge_key() triggered, sending out munge key on all relations!!')
        for rel in self.relations:
            #rel.to_publish.update({'munge_key': self._exposed_munge_key})
            rel.to_publish.update({'munge_key': leadership.leader_get('munge_key')})
        flags.clear_flag(self.expand_name(
            'endpoint.{endpoint_name}.changed'))
        hookenv.log('provide_munge_key(): munge key published on endpoint in MungeAuthProvides')

    # TODO: Should not be done in the interface?
    # Should we distinguish between providing munge keys to all relations (as the function above)
    # or just the currently joined unit?
    @reactive.when('endpoint.{endpoint_name}.changed')
    @reactive.when('leadership.set.munge_key')
    def new_munge_consumer(self):
        remote_unit = hookenv.remote_unit()
        if remote_unit:
            mk = leadership.leader_get('munge_key')
            hookenv.log('new_munge_consumer(): join event from %s, publishing key: %s' % (remote_unit, mk))
            #rel = self.relation[remote_unit]
            #rel.to_publish.update({'munge_key': mk})