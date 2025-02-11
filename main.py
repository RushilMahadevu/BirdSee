def parse_ebd(file_path):
    species_counts = defaultdict(int)
    locations = defaultdict(set)
    dates = set()
    observations = []

    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        for row in reader:
            species = row['COMMON NAME']
            location = row['LOCALITY']
            date = row['OBSERVATION DATE']
            count = int(row['OBSERVATION COUNT']) if row['OBSERVATION COUNT'].isdigit() else 0

            species_counts[species] += count
            locations[species].add(location)
            dates.add(date)
            observations.append(row)

    def analyze_by_date(observations):
        date_counts = defaultdict(set)
        for obs in observations:
            date = obs['OBSERVATION DATE']
            species = obs['COMMON NAME']
            date_counts[date].add(species)
        return date_counts

    def analyze_hotspots(observations):
        hotspots = defaultdict(set)
        for obs in observations:
            location = obs['LOCALITY']
            species = obs['COMMON NAME']
            hotspots[location].add(species)
        return hotspots

    def observer_stats(observations):
        observers = defaultdict(set)
        for obs in observations:
            observer_id = obs['OBSERVER ID']
            species = obs['COMMON NAME']
            observers[observer_id].add(species)
        return observers

    def analyze_time_of_day(observations):
        time_counts = {
            'Morning': 0,   # 5-11
            'Afternoon': 0, # 12-16
            'Evening': 0,   # 17-20
            'Night': 0      # 21-4
        }
        for obs in observations:
            time = obs['TIME OBSERVATIONS STARTED']
            if time:
                hour = int(time.split(':')[0])
                if 5 <= hour <= 11:
                    time_counts['Morning'] += 1
                elif 12 <= hour <= 16:
                    time_counts['Afternoon'] += 1
                elif 17 <= hour <= 20:
                    time_counts['Evening'] += 1
                else:
                    time_counts['Night'] += 1
        return time_counts

    date_counts = analyze_by_date(observations)
    hotspots = analyze_hotspots(observations)
    observer_data = observer_stats(observations)
    time_data = analyze_time_of_day(observations)

    while True:
        print("\nSelect sorting option:")
        print("1. Most observed species")
        print("2. Species with most locations")
        print("3. Most species-rich dates")
        print("4. Observation hotspots")
        print("5. Observer statistics")
        print("6. Time of day analysis")
        print("7. Exit")
        
        choice = input("Enter choice (1-7): ")
        
        def display_sorted_data(data, n, key_func, format_func):
            for item in sorted(data, key=key_func, reverse=True)[:n]:
                print(format_func(item))

        if choice == '1':
            n = int(input("How many species to display? "))
            display_sorted_data(
                species_counts.items(),
                n,
                key_func=lambda x: x[1],
                format_func=lambda x: f"{x[0]}: {x[1]} birds, seen at {len(locations[x[0]])} locations"
            )

        elif choice == '2':
            n = int(input("How many species to display? "))
            display_sorted_data(
                locations,
                n, 
                key_func=lambda x: len(locations[x]),
                format_func=lambda x: f"{x}: seen at {len(locations[x])} locations, {species_counts[x]} total birds"
            )

        elif choice == '3':
            n = int(input("How many dates to display? "))
            display_sorted_data(
                date_counts.items(),
                n,
                key_func=lambda x: len(x[1]),
                format_func=lambda x: f"{x[0]}: {len(x[1])} different species"
            )

        elif choice == '4':
            n = int(input("How many hotspots to display? "))
            display_sorted_data(
                hotspots.items(),
                n,
                key_func=lambda x: len(x[1]),
                format_func=lambda x: f"{x[0]}: {len(x[1])} different species"
            )

        elif choice == '5':
            n = int(input("How many observers to display? "))
            display_sorted_data(
                observer_data.items(),
                n,
                key_func=lambda x: len(x[1]),
                format_func=lambda x: f"Observer {x[0]}: {len(x[1])} different species"
            )

        elif choice == '6':
            for period, count in time_data.items():
                print(f"{period}: {count} observations")

        elif choice == '7':
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    import csv
    from collections import defaultdict

    file_path = 'ebd.txt'
    parse_ebd(file_path)