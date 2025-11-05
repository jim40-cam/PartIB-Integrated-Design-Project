def parse_qr(code_str):
  
    try:
        parts = [p.strip() for p in code_str.split(',')]
        rack_str = parts[0].split()[-1].upper()   # A or B
        level_str = parts[1].capitalize()         # Upper or Lower
        pos = int(parts[2])                       # 1–6

        # Convert to compact form
        level_short = 'L' if level_str == 'Lower' else 'U' if level_str == 'Upper' else None

        if rack_str in ('A', 'B') and level_short in ('L', 'U') and 1 <= pos <= 6:
            parsed = (rack_str, level_short, pos)
            print(parsed)
            return parsed
            
        else:
            print(f"Invalid QR code format: {code_str}")
            return None

    except Exception as e:
        print(f"Error parsing QR code '{code_str}': {e}")
        return None


parse_qr("Rack A, Lower, 6")