import sys
import traceback
import time
from awsiot.greengrasscoreipc.clientv2 import GreengrassCoreIPCClientV2
from localpubsub import publisher, subscriber
import json

def main():
    args = sys.argv[1:]
    topic = args[0]
    message = " ".join(args[1:])
    #topic = "+/emission/data"
    topic1 = "iot/vehicle1"
    #message = "Testing"
    try:
        ipc_client = GreengrassCoreIPCClientV2()
        # Subscribe to the topic before publishing
        subscriber.subscribe_to_topic(ipc_client, topic)
        try:
            subscriber.subscribe_to_topic(ipc_client, "+/emission/data")
        except Exception:
            print("Exception occurred", file=sys.stderr)
            traceback.print_exc()
        # Publish a message for N times and exit
        publisher.publish_message_N_times(ipc_client, topic, message)
        while True:
            time.sleep(10)
            print("Process is still running fine...")
            try:
                print(f'{{"max_CO2": {subscriber.MyClass.maxCounter}}}')
                publisher.publish_message_N_times(ipc_client,topic1, f'{{"max_CO2": {subscriber.MyClass.maxCounter}}}',1)                
            except Exception:
                print("Exception occurred", file=sys.stderr)
                traceback.print_exc()  
            
    except Exception:
        print("Exception occurred", file=sys.stderr)
        traceback.print_exc()
        exit(1)


if __name__ == "__main__":
    main()
