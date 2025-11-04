# Routes from a pickup location to a rack position

#intakes "parsed" tuple from scan_qr_code and returns "frl" string in "location" free variable
yellow_locations_routes = {
    ("A", "L", 1): "lfffrffffffrf",        #from T junction to end of dropping line
    ("A", "L", 2): "lfffrfffffrf",
    ("A", "L", 3): "lfffrffffrf",
    ("A", "L", 4): "lfffrfffrf",
    ("A", "L", 5): "lfffrffrf",
    ("A", "L", 6): "lfffrfrf",
    ("A", "U", 1): "rflfffffffflflfrfrflf",
    ("A", "U", 2): "rflfffffffflflfrfrfflf",
    ("A", "U", 3): "rflfffffffflflfrfrffflf",
    ("A", "U", 4): "rflfffffffflflfrfrfffflf",
    ("A", "U", 5): "rflfffffffflflfrfrffffflf",
    ("A", "U", 6): "rflfffffffflflfrfrfffffflf",
    ("B", "L", 1): "rflflf",
    ("B", "L", 2): "rflfflf",
    ("B", "L", 3): "rflffflf",
    ("B", "L", 4): "rflfffflf",
    ("B", "L", 5): "rflffffflf",
    ("B", "L", 6): "rflfffffflf",
    ("B", "U", 1): "rflfffffffflflflflffffffrf",
    ("B", "U", 2): "rflfffffffflflflflfffffrf",
    ("B", "U", 3): "rflfffffffflflflflffffrf",
    ("B", "U", 4): "rflfffffffflflflflfffrf",
    ("B", "U", 5): "rflfffffffflflflflffrf",
    ("B", "U", 6): "rflfffffffflflflflfrf" }

red_locations_routes = {
    ("A", "L", 1): "lfrlfffrffffffrf",        #from T junction to end of dropping line
    ("A", "L", 2): "lfrlfffrfffffrf",
    ("A", "L", 3): "lfrlfffrffffrf",
    ("A", "L", 4): "lfrlfffrfffrf",
    ("A", "L", 5): "lfrlfffrffrf",
    ("A", "L", 6): "lfrlfffrfrf",
    ("A", "U", 1): "rflfffffffflflfrfrflf",
    ("A", "U", 2): "rflfffffffflflfrfrfflf",
    ("A", "U", 3): "rflfffffffflflfrfrffflf",
    ("A", "U", 4): "rflfffffffflflfrfrfffflf",
    ("A", "U", 5): "rflfffffffflflfrfrffffflf",
    ("A", "U", 6): "rflfffffffflflfrfrfffffflf",
    ("B", "L", 1): "rflflf",
    ("B", "L", 2): "rflfflf",
    ("B", "L", 3): "rflffflf",
    ("B", "L", 4): "rflfffflf",
    ("B", "L", 5): "rflffffflf",
    ("B", "L", 6): "rflfffffflf",
    ("B", "U", 1): "rflfffffffflflflflffffffrf",
    ("B", "U", 2): "rflfffffffflflflflfffffrf",
    ("B", "U", 3): "rflfffffffflflflflffffrf",
    ("B", "U", 4): "rflfffffffflflflflfffrf",
    ("B", "U", 5): "rflfffffffflflflflffrf",
    ("B", "U", 6): "rflfffffffflflflflfrf" }

#Green routes are just symmetrical to yellow's about the median (y) axis. Same for Blue and Red. 
 #A becomes B, r becomes l, 1 becomes 6 (2 becomes 5, etc). Vis-versa
#Ex: Yellow: ("B", "L", 1): "rflflf", becomes Green: ("A", "L", 6): "lfrfrf"

green_location_routes = {
    ("B", "L", 1): "rffflflf",        
    ("B", "L", 2): "rffflfflf",       
    ("B", "L", 3): "rffflffflf",      
    ("B", "L", 4): "rffflfffflf",    
    ("B", "L", 5): "rffflffffflf",    
    ("B", "L", 6): "rffflfffffflf",   

    ("B", "U", 1): "lfrffffffffrfrflflffffffrf",  # from ("A","U",6)
    ("B", "U", 2): "lfrffffffffrfrflflfffffrf",   # from ("A","U",5)
    ("B", "U", 3): "lfrffffffffrfrflflffffrf",    # from ("A","U",4)
    ("B", "U", 4): "lfrffffffffrfrflflfffrf",     # from ("A","U",3)
    ("B", "U", 5): "lfrffffffffrfrflflffrf",      # from ("A","U",2)
    ("B", "U", 6): "lfrffffffffrfrflflfrf",       # from ("A","U",1)

    
    ("A", "L", 1): "lfrffffffrf",     # from ("B","L",6)
    ("A", "L", 2): "lfrfffffrf",      # from ("B","L",5)
    ("A", "L", 3): "lfrffffrf",       # from ("B","L",4)
    ("A", "L", 4): "lfrfffrf",        # from ("B","L",3)
    ("A", "L", 5): "lfrffrf",         # from ("B","L",2)
    ("A", "L", 6): "lfrfrf",          # from ("B","L",1)

    ("A", "U", 1): "lfrffffffffrfrfrfrfffffflf",  # from ("B","U",6)
    ("A", "U", 2): "lfrffffffffrfrfrfrffffflf",   # from ("B","U",5)
    ("A", "U", 3): "lfrffffffffrfrfrfrfffflf",    # from ("B","U",4)
    ("A", "U", 4): "lfrffffffffrfrfrfrffflf",     # from ("B","U",3)
    ("A", "U", 5): "lfrffffffffrfrfrfrfflf",      # from ("B","U",2)
    ("A", "U", 6): "lfrffffffffrfrfrfrflf",       # from ("B","U",1),
}


blue_location_routes = {
    ("B", "L", 6): "rffflfffffflf",
    ("B", "L", 5): "rffflffffflf",
    ("B", "L", 4): "rffflfffflf",
    ("B", "L", 3): "rffflffflf",
    ("B", "L", 2): "rffflfflf",
    ("B", "L", 1): "rffflflf",
    ("B", "U", 6): "lfrffffffffrfrflflfrf",
    ("B", "U", 5): "lfrffffffffrfrflflffrf",
    ("B", "U", 4): "lfrffffffffrfrflflfffrf",
    ("B", "U", 3): "lfrffffffffrfrflflffffrf",
    ("B", "U", 2): "lfrffffffffrfrflflfffffrf",
    ("B", "U", 1): "lfrffffffffrfrflflffffffrf",
    ("A", "L", 6): "lfrfrf",
    ("A", "L", 5): "lfrffrf",
    ("A", "L", 4): "lfrfffrf",
    ("A", "L", 3): "lfrffffrf",
    ("A", "L", 2): "lfrfffffrf",
    ("A", "L", 1): "lfrffffffrf",
    ("A", "U", 6): "lfrffffffffrfrfrfrfffffflf",
    ("A", "U", 5): "lfrffffffffrfrfrfrffffflf",
    ("A", "U", 4): "lfrffffffffrfrfrfrfffflf",
    ("A", "U", 3): "lfrffffffffrfrfrfrffflf",
    ("A", "U", 2): "lfrffffffffrfrfrfrfflf",
    ("A", "U", 1): "lfrffffffffrfrfrfrflf",
}
