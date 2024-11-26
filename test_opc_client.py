from asyncua import Client
import asyncio
import logging
from datetime import datetime

async def test_tag_read(client, tag_name):
    """Test reading a specific tag"""
    try:
        # Fixed path to include PJ_OD91_01 folder
        node = client.get_node(f"ns=2;s=PJ_OD91_01/{tag_name}")
        value = await node.read_value()
        print(f"{tag_name}: {value}")
        return True
    except Exception as e:
        print(f"Error reading {tag_name}: {e}")
        return False

async def monitor_tags():
    url = "opc.tcp://localhost:4840/freeopcua/server/"
    
    try:
        async with Client(url) as client:
            print(f"\nConnected to OPC UA Server at {url}")
            print("=" * 50)
            
            # Tags match exactly with server names
            tags_to_monitor = ['spm', 'motor_amps', 'production_rate']
            
            while True:
                print(f"\nTime: {datetime.now().strftime('%H:%M:%S')}")
                print("-" * 30)
                
                results = []
                for tag in tags_to_monitor:
                    result = await test_tag_read(client, tag)
                    results.append(result)
                success = all(results)
                
                if not success:
                    print("Some tags failed to read!")
                
                await asyncio.sleep(2)
                
    except Exception as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("Starting OPC UA Client Test...")
    print("Press Ctrl+C to stop")
    
    try:
        asyncio.run(monitor_tags())
    except KeyboardInterrupt:
        print("\nTest client stopped by user")
    except Exception as e:
        print(f"Error: {e}")