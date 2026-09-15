// ─────────────────────────────────────────────
// BANDS IN BEND — Weekly Show Data
// Update this file each week to refresh the site
// ─────────────────────────────────────────────

const WEEK = {
  label: "September 14 – 20",
  year: "2026",
};

const SHOWS = [
  {
    day: "Monday",
    date: "September 14",
    shows: [
      { artist: "Bluegrass Collective", venue: "Silver Moon Brewing", time: "6pm" },
      { artist: "Open Mic & Jam", venue: "Bunk+Brew", time: "6pm" },
      { artist: "Open Mic hosted by John Reach ft. Sireniti", venue: "The Astro Lounge", time: "8pm-12am" },
    ],
  },
  {
    day: "Tuesday",
    date: "September 15",
    shows: [
      { artist: "Lava Butte Boys", venue: "Cassity's Bar & Grill", time: "5pm" },
      { artist: "Fluffalove", venue: "Greg's Grill", time: "5pm" },
      { artist: "Oregon Fryer", venue: "Trailhead Lodge", time: "5pm" },
      { artist: "Use'Ta Do - Hank Williams Sr. Celebration", venue: "Goodlife Brewing Company", time: "6pm" },
      { artist: "Obsidian Jazz", venue: "The Commonwealth Pub", time: "7pm" },
    ],
  },
  {
    day: "Wednesday",
    date: "September 16",
    shows: [
      { artist: "Chris Huffine", venue: "Austin Kitchen Wine Bar & Mercantile", time: "5pm" },
      { artist: "Ghost of Brian Craig", venue: "Crosscut Warming Hut No. 5", time: "6pm" },
      { artist: "Jenna Hansen", venue: "The Bite", time: "6pm" },
      { artist: "Mason James & Samantha Hart", venue: "Basecamp Bend", time: "6pm" },
      { artist: "Rushadicus & Vacancy Floor", venue: "Silver Moon Brewing", time: "6pm" },
      { artist: "Open Mic w/ Derek Michael Marc", venue: "Northside Bar & Grill", time: "6pm" },
      { artist: "Musicians Open Showcase", venue: "The Commonwealth Pub", time: "6pm" },
      { artist: "Tony Smiley", venue: "Father Luke's Room", time: "7pm" },
    ],
  },
  {
    day: "Thursday",
    date: "September 17",
    shows: [
      { artist: "Lava Butte Boys", venue: "Austin Kitchen Wine Bar & Mercantile", time: "5pm" },
      { artist: "Charlee Prayers", venue: "Mountain Burger", time: "6pm" },
      { artist: "Draven Schmidt", venue: "The Lot", time: "6pm" },
      { artist: "Open Mic hosted by Mason James", venue: "Teal Tea & Art Lounge", time: "6pm" },
      { artist: "Sakoyana", venue: "Rivers Place Taphouse", time: "6pm" },
      { artist: "Soul'd Out", venue: "Stoller Wine Bar", time: "6pm" },
      { artist: "Vieux Farka Tourè & Muhlaika", venue: "The Domino Room", time: "7pm" },
      { artist: "Whipsaw ft. members of Hillstomp & The Taxpayers", venue: "Silver Moon Brewing", time: "7pm" },
      { artist: "Led Zepagain", venue: "Tower Theatre", time: "7:30pm" },
      { artist: "Jared McComas", venue: "The Stihl Whiskey Bar", time: "8pm" },
      { artist: "Doc Ryan and The Rowdy Boys", venue: "The Commonwealth Pub", time: "8:30pm" },
    ],
  },
  {
    day: "Friday",
    date: "September 18",
    shows: [
      { artist: "Heller Highwater", venue: "Pine Nursery Park", time: "5pm" },
      { artist: "Bill Powers", venue: "Bend Cider Co.", time: "6pm" },
      { artist: "Cold River Music Band", venue: "Wetlands Taphouse", time: "6pm" },
      { artist: "Heaven Zest w/ Skip Wicked & Emily Turner", venue: "Volcanic Theatre Pub", time: "6pm" },
      { artist: "Joyful Lane", venue: "Lazy Z Ranch", time: "6pm" },
      { artist: "Lickety Split", venue: "Runaround Sue Barbecue", time: "6pm" },
      { artist: "Riley Green w/ Randy Houser, Kushus Culpepper & Hannah McFarland", venue: "Hayden Homes Amphitheater", time: "6pm" },
      { artist: "Chained To Stone", venue: "Blacksmith Public House", time: "6:30pm" },
      { artist: "Langdon Bradley", venue: "Silver Moon Brewing", time: "7pm" },
      { artist: "American Aquarium", venue: "Silver Moon Brewing", time: "7pm" },
      { artist: "MFG", venue: "Silver Moon Brewing", time: "7pm" },
      { artist: "Mark Ransom", venue: "Currents at Riverhouse Lodge", time: "7pm" },
      { artist: "Sean McLean and the Vibetenders", venue: "Father Luke's Room", time: "7pm" },
      { artist: "The Hasbens & Sakoyana", venue: "The Commonwealth Pub", time: "8pm" },
      { artist: "DJ Raider Mystic", venue: "The Coyote", time: "9pm" },
      { artist: "DJ Timothy Bee", venue: "Dogwood at The Pine Shed", time: "9pm" },
      { artist: "Suckerpunch w/ Street Teeth & Burn The Wolf", venue: "M&J Tavern", time: "9pm" },
    ],
  },
  {
    day: "Saturday",
    date: "September 19",
    shows: [
      { artist: "Polkatones, Funk Around & Find Out, & Party In The Back", venue: "Worthy Brewing", time: "1-9pm" },
      { artist: "Will Grove, Atillion, Elle Jay, Sisu, Robot Mushroom, Joel Chadd + MORE", venue: "Bunk+Brew", time: "3-11pm" },
      { artist: "Precious Byrd, Rubbah Tree, Amargoso & DJ Indica Jones", venue: "10 Barrel East Side Pub", time: "4-9pm" },
      { artist: "Jack Krouscoup Quartet", venue: "Stoller Wine Bar", time: "5pm" },
      { artist: "Sugar Mountain", venue: "Austin Kitchen Wine Bar & Mercantile", time: "5pm" },
      { artist: "SPINA w/ Acidic Decay & Ephixis", venue: "The Capitol", time: "5:30pm" },
      { artist: "Crosscut Blues", venue: "The Bite", time: "6pm" },
      { artist: "The Positive Side Jazz Band", venue: "Boneyard Pub", time: "6pm" },
      { artist: "Old Growth Band", venue: "Century Commons Taps & Trucks", time: "6pm" },
      { artist: "Kurt Silva & Cynthia West", venue: "Portello Lounge", time: "6:30pm" },
      { artist: "Schwing", venue: "Blacksmith Public House", time: "6:30pm" },
      { artist: "Fisarmonicats", venue: "Bend Oktoberfest", time: "7pm" },
      { artist: "Luke Bower", venue: "The Fellowship at Bend", time: "7pm" },
      { artist: "That 90's Band", venue: "Silver Moon Brewing", time: "7pm" },
      { artist: "Queen: It's Kinda Magic ft. Warren Vernon-Driscoll", venue: "Tower Theatre", time: "7:30pm" },
      { artist: "Bass In Bend ft. SYLK, ROMZ, PANDA, BEAM & ZYNTH", venue: "Volcanic Theatre Pub", time: "8pm" },
      { artist: "Chiggi Momo", venue: "Teal Tea & Art Lounge", time: "8pm" },
      { artist: "The Jugulars", venue: "Northside Bar & Grill", time: "8pm" },
      { artist: "Thievery Corporation w/ DJ Mystic", venue: "Midtown Ballroom", time: "8pm" },
      { artist: "The Rumpeppers", venue: "The Commonwealth Pub", time: "8pm" },
      { artist: "DJ Humblebeatz", venue: "The Coyote", time: "9pm" },
      { artist: "DJ Mark Brody", venue: "Dogwood at The Pine Shed", time: "9pm" },
      { artist: "DJ McLovin", venue: "General Duffy's Waterhole", time: "9pm" },
      { artist: "Yemanjo! - A Thievery Corporation after party", venue: "Midtown Ballroom Annex", time: "11pm" },
    ],
  },
  {
    day: "Sunday",
    date: "September 20",
    shows: [
      { artist: "Aslin", venue: "Currents at Riverhouse Lodge", time: "11am" },
      { artist: "Annika Hankshaw", venue: "Goodlife Brewing Company", time: "4pm" },
      { artist: "Mason James & Samantha Hart", venue: "Ballers & Brews", time: "4pm" },
      { artist: "Open Mic on the Moon", venue: "Silver Moon Brewing", time: "5-8pm" },
      { artist: "Bleachers w/ The Linda Lindas", venue: "Hayden Homes Amphitheater", time: "6:30pm" },
      { artist: "The Lone Bellow & The Living Room", venue: "The Domino Room", time: "7pm" },
      { artist: "Shemekia Copeland", venue: "Tower Theatre", time: "7:30pm" },
    ],
  },
];

// Highlights shown on the cover — update each week
const HIGHLIGHTS = [
  { artist: "Oregon Fryer", day: "Tue Sep 15" },
  { artist: "Vieux Farka Tourè", day: "Thu Sep 17" },
  { artist: "Riley Green", day: "Fri Sep 18" },
  { artist: "Atillion & Robot Mushroom", day: "Sat Sep 19" },
  { artist: "Bleachers", day: "Sun Sep 20" },
];
