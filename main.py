def parse_ebd(file_path):
    species_counts = defaultdict(int)
    locations = defaultdict(set)
    dates = set()

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

    while True:
        print("\nSelect sorting option:")
        print("1. Most observed species")
        print("2. Species with most locations")
        print("3. Exit")
        
        choice = input("Enter choice (1-3): ")
        
        def get_species_count(item):
            return item[1]

        def format_species_output(item):
            species = item
            count = item
            return f"{species}: {count} birds, seen at {len(locations[species])} locations"

        def get_location_count(species):
            return len(locations[species])

        def format_location_output(species):
            return f"{species}: seen at {len(locations[species])} locations, {species_counts[species]} total birds"

        def display_sorted_data(data, n, key_func, format_func):
            for item in sorted(data, key=key_func, reverse=True)[:n]:
                print(format_func(item))

        if choice == '1':
            n = int(input("How many species to display? "))
            display_sorted_data(
                species_counts.items(),
                n,
                key_func=get_species_count,
                format_func=format_species_output
            )

        elif choice == '2':
            n = int(input("How many species to display? "))
            display_sorted_data(
                locations,
                n,
                key_func=get_location_count,
                format_func=format_location_output
            )

        elif choice == '3':
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    import csv
    from collections import defaultdict

    file_path = 'ebd.txt'
    parse_ebd(file_path)