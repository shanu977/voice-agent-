import sounddevice as sd


def list_output_devices():
    devices = sd.query_devices()
    output_devices = []
    for index, device in enumerate(devices):
        if device["max_output_channels"] > 0:
            output_devices.append({
                "index": index,
                "name": device["name"],
                "channels": device["max_output_channels"],
                "default_samplerate": device["default_samplerate"]
            })
    return output_devices


def select_output_device():
    devices = list_output_devices()

    if not devices:
        print("No output devices found!")
        return None

    print("\n" + "=" * 60)
    print("AUDIO OUTPUT DEVICE SELECTION")
    print("=" * 60)
    print("Available output devices:\n")

    headphones = []
    speakers = []
    other = []

    for d in devices:
        name_lower = d["name"].lower()
        if any(keyword in name_lower for keyword in ["headphone", "headset", "earphone", "earbud", "wh-", "buds", "airpods"]):
            headphones.append(d)
        elif any(keyword in name_lower for keyword in ["speaker", "realtek", "sound mapper", "primary sound driver"]):
            speakers.append(d)
        else:
            other.append(d)

    device_map = {}
    idx = 1

    if headphones:
        print("HEADPHONES / HEADSETS:")
        for d in headphones:
            print(f"  {idx}. {d['name']} ({d['channels']} ch)")
            device_map[idx] = d["index"]
            idx += 1
        print()

    if speakers:
        print("SPEAKERS:")
        for d in speakers:
            print(f"  {idx}. {d['name']} ({d['channels']} ch)")
            device_map[idx] = d["index"]
            idx += 1
        print()

    if other:
        print("OTHER:")
        for d in other:
            print(f"  {idx}. {d['name']} ({d['channels']} ch)")
            device_map[idx] = d["index"]
            idx += 1
        print()

    default_idx = sd.default.device[1]
    default_name = sd.query_devices(default_idx)["name"]
    print(f"System default: {default_name} (index {default_idx})")
    print()

    while True:
        try:
            choice = input(f"Select device [1-{len(device_map)}] or press Enter for default: ").strip()

            if choice == "":
                print(f"Using system default: {default_name}")
                return default_idx

            choice_idx = int(choice)
            if choice_idx in device_map:
                selected_device_idx = device_map[choice_idx]
                selected_name = sd.query_devices(selected_device_idx)["name"]
                print(f"Selected: {selected_name}")
                return selected_device_idx
            else:
                print(f"Invalid choice. Please enter 1-{len(device_map)} or press Enter.")
        except ValueError:
            print("Please enter a number or press Enter.")
        except KeyboardInterrupt:
            print("\nUsing system default.")
            return default_idx


if __name__ == "__main__":
    selected = select_output_device()
    if selected is not None:
        print(f"\nSelected device index: {selected}")