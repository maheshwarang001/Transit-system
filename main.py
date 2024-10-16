import argparse

from src.mass_transit_billing import MassTransitBilling


def main():
    parser = argparse.ArgumentParser(description="Process mass transit billing.")
    parser.add_argument("zone_path", type=str, help="Path to the zone map CSV file")
    parser.add_argument("journey_path", type=str, help="Path to the journey data CSV file")
    parser.add_argument("output_path", type=str, help="Path to the output data CSV file")

    args = parser.parse_args()

    billing_system = MassTransitBilling(args.journey_path, args.zone_path,args.output_path)
    billing_system.run()

if __name__ == "__main__":
    main()
