import charms.reactive.flags as flags
import charms.reactive as reactive
import charmhelpers.core.hookenv as hookenv


class MungeAuthRequires(reactive.Endpoint):

    def _local_munge_key(self):
        self._cached_munge_key = hookenv.config().get('munge_key')
    
    def _munge_auth_relation(self):
        # can only be related to a single munge provider
        assert len(self.relations) < 2
        return self.relations[0]

    @reactive.when('endpoint.{endpoint_name}.changed.munge_key')
    def check_key(self):
        rel = self._munge_auth_relation()
        joined_units = rel.joined_units
        hookenv.log('Joined munge provider units: {}'.format(joined_units))
        remote_unit = hookenv.remote_unit()
        hookenv.log('Remote unit: {}'.format(remote_unit))
        remote_munge_key = joined_units[remote_unit].received.get('munge_key')
        # update a munge key if it's different from a local one
        # there were no per-application endpoint buckets at the time of writing
        # implemented in Juju
        self._local_munge_key()
        if remote_munge_key and remote_munge_key != self._cached_munge_key:
            self._cached_munge_key = remote_munge_key
            flags.set_flag(self.expand_name(
                'endpoint.{endpoint_name}.munge_key_updated'))
        flags.clear_flag('endpoint.munge-consumer.changed.munge_key')

    @property
    def munge_key(self):
        return self._cached_munge_key
