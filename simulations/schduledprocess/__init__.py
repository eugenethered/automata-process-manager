from cache.holder.RedisCacheHolder import RedisCacheHolder

from simulations.schduledprocess.SimulatedScheduledProcess import SimulatedScheduledProcess

if __name__ == '__main__':

    options = {
        'REDIS_SERVER_ADDRESS': '192.168.1.90',
        'REDIS_SERVER_PORT': 6379,
        'PROCESS_KEY': '{}:process:status:{}',
        'PROCESS_RUN_PROFILE_KEY': '{}:process:run-profile:{}'
    }

    RedisCacheHolder(options)

    scheduled_process = SimulatedScheduledProcess(options, 'test', 'simulation')
    scheduled_process.start_process_schedule()
