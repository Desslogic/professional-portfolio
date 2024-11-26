from asyncua import Server, ua
import asyncio
import logging
from datetime import datetime
from pumpjack_simulator import PumpJackSimulator

class PumpJackOPCServer:
    def __init__(self, endpoint="opc.tcp://0.0.0.0:4840/freeopcua/server/"):
        self.endpoint = endpoint
        self.server = Server()
        self.simulator = PumpJackSimulator()
        self.namespace = "http://examples.freeopcua.github.io"

    def convert_value(self, value, target_type):
        """Convert values to correct OPC UA types with error handling"""
        try:
            if target_type == ua.VariantType.Double:
                return float(value)
            elif target_type == ua.VariantType.Boolean:
                return bool(value)
            elif target_type == ua.VariantType.Int32:
                return int(value)
            else:
                return value
        except (ValueError, TypeError) as e:
            logging.error(f"Value conversion error: {e}")
            return 0.0  # Safe default

    async def init_server(self):
        """Initialize OPC UA server with correct data types"""
        await self.server.init()
        self.server.set_endpoint(self.endpoint)

        await self.server.set_build_info(
            product_uri="PumpJack-Simulator",
            manufacturer_name="Training",
            product_name="PumpJack OPC Server",
            software_version="1.0",
            build_number="1",
            build_date=datetime.now()
        )

        idx = await self.server.register_namespace(self.namespace)
        objects = self.server.nodes.objects
        self.pj_folder = await objects.add_folder(idx, "PJ_OD91_01")

        # Define tags with proper types
        self.tags = {
            'spm': await self.pj_folder.add_variable(idx, 'spm', 0.0, varianttype=ua.VariantType.Double),
            'motor_amps': await self.pj_folder.add_variable(idx, 'motor_amps', 0.0, varianttype=ua.VariantType.Double),
            # Add other tags with appropriate types
        }

        # Make some tags writable
        await self.tags['spm'].set_writable()

    async def update_tags(self):
        """Update OPC UA tags with type conversion and error handling"""
        self.simulator.start()

        while True:
            try:
                state = self.simulator.simulate_step()

                for tag_name, tag_node in self.tags.items():
                    if tag_name in state:
                        value = state[tag_name]
                        variant_type = (await tag_node.read_data_type_as_variant_type())
                        converted_value = self.convert_value(value, variant_type)
                        await tag_node.write_value(converted_value)

            except Exception as e:
                logging.error(f"Error updating tags: {e}")

            await asyncio.sleep(1)

    async def start(self):
        """Start the OPC UA server with error handling"""
        try:
            await self.init_server()
            async with self.server:
                print(f"Server started at {self.endpoint}")
                print("Available tags:")
                for name in self.tags:
                    print(f"  - {name}")
                await self.update_tags()
        except Exception as e:
            logging.error(f"Server error: {e}")
            raise

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    server = PumpJackOPCServer()
    try:
        asyncio.run(server.start())
    except KeyboardInterrupt:
        logging.info("Server stopped by user")
    except Exception as e:
        logging.error(f"Server error: {e}")