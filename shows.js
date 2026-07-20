// ─────────────────────────────────────────────
// BANDS IN BEND — Weekly Show Data
// Update this file each week to refresh the site
// ─────────────────────────────────────────────

const WEEK = {
  label: "July 20 – 26",
  year: "2026",
};

const SHOWS = [
  {
    day: "Monday",
    date: "July 20",
    shows: [
      { artist: "Bluegrass Collective", venue: "Silver Moon Brewing", time: "6pm" },
      { artist: "Mari & The Dream", venue: "On Tap", time: "6pm" },
      { artist: "Musicians Open Showcase", venue: "The Commonwealth Pub", time: "4pm" },
      { artist: "Weekly Live Music", venue: "Bend Brewing Company", time: "6pm" },
    ],
  },
  {
    day: "Tuesday",
    date: "July 21",
    shows: [
      { artist: "Elise Franklin Quartet", venue: "The Commonwealth Pub", time: "7pm" },
      { artist: "The Jaws of Brooklyn w/ Double Jump & Jordan Wolfe", venue: "Silver Moon Brewing", time: "6:30pm" },
      { artist: "Open Mic w/ Mari", venue: "The Cellar", time: "6pm" },
      { artist: "Pete Bush", venue: "Goodlife Brewing Company", time: "6pm" },
      { artist: "Vern Johnson", venue: "Deschutes Brewery Beer Garden", time: "7pm" },
      { artist: "Weekly Live Music", venue: "Greg's Grill", time: "6pm" },
    ],
  },
  {
    day: "Wednesday",
    date: "July 22",
    shows: [
      { artist: "Aslin w/ Frecks & Aiden Moye", venue: "Silver Moon Brewing", time: "7pm" },
      { artist: "Bill Powers", venue: "Crosscut Warming Hut No. 5", time: "6pm" },
      { artist: "Deone Jennings", venue: "Tetherow Resort", time: "5pm" },
      { artist: "Doc Monos", venue: "Austin Kitchen Wine Bar & Mercantile", time: "5pm" },
      { artist: "Elevator Operator", venue: "The Commonwealth Pub", time: "7:30pm" },
      { artist: "Jerry Garcia Band Night: Steelhead & The Soul Sistahs, G-Bots & The Journeymen", venue: "Silver Moon Brewing", time: "7pm" },
      { artist: "MATTE BLVCK - House Of Serpents Tour", venue: "Volcanic Theatre Pub", time: "9pm" },
      { artist: "Pete Kartsounes", venue: "Father Luke's Room", time: "7pm" },
    ],
  },
  {
    day: "Thursday",
    date: "July 23",
    shows: [
      { artist: "Bill Powers", venue: "Mountain Burger", time: "6pm" },
      { artist: "Broken Top Duo", venue: "Austin Kitchen Wine Bar & Mercantile", time: "5pm" },
      { artist: "Carson Hackbart", venue: "The Coyote", time: "5pm" },
      { artist: "Derek Michael Marc", venue: "Stoller Wine Bar", time: "6pm" },
      { artist: "Doc Ryan Band", venue: "Rivers Place Taphouse", time: "6pm" },
      { artist: "Dry Canyon Stampede", venue: "The Grove Market Hall", time: "6pm" },
      { artist: "Fireside Collective & Wild Hare", venue: "Silver Moon Brewing", time: "7pm" },
      { artist: "Irish Traditional Music", venue: "The Cellar", time: "6pm" },
      { artist: "Kimberly June \"KJ\"", venue: "The Lot", time: "6pm" },
      { artist: "Left On Red", venue: "Northside Bar & Grill", time: "7pm" },
      { artist: "Long Gone Wilder", venue: "Bevel Craft Brewing", time: "6pm" },
      { artist: "Queen Mother w/ Baduko and Bahuro Marimba", venue: "Drake Park Munch & Music", time: "5:30pm" },
      { artist: "Richard Taelour Band", venue: "The Commonwealth Pub", time: "7:30pm" },
      { artist: "Wynonna Judd & Melissa Etheridge", venue: "Hayden Homes Amphitheater", time: "6:30pm" },
    ],
  },
  {
    day: "Friday",
    date: "July 24",
    shows: [
      { artist: "Angelic Noise", venue: "Riverhouse Lodge", time: "7pm" },
      { artist: "Chiggi Momo", venue: "Worthy Brewing", time: "7pm" },
      { artist: "The Desert Howlers", venue: "M&J Tavern", time: "9pm" },
      { artist: "The Dirty Grass Players", venue: "Silver Moon Brewing", time: "7pm" },
      { artist: "DJ Nym", venue: "Dogwood at The Pine Shed", time: "9pm" },
      { artist: "Dom Ruben", venue: "The Cellar", time: "6pm" },
      { artist: "Dry Canyon Stampede", venue: "Boneyard Pub", time: "6pm" },
      { artist: "Futurebirds w/ Deloyd Elze", venue: "Volcanic Theatre Pub", time: "7pm" },
      { artist: "Gravewitch, Torn From Ashes, Within The Pyre & Cryptic Divination", venue: "Silver Moon Brewing", time: "6pm" },
      { artist: "Jordan Davis", venue: "Hayden Homes Amphitheater", time: "7:30pm" },
      { artist: "Pina Colada", venue: "Portello Wine Cafe", time: "6:30pm" },
      { artist: "Rusty Frets", venue: "The Grove Market Hall", time: "6pm" },
      { artist: "SHINE", venue: "The Commonwealth Pub", time: "8pm" },
    ],
  },
  {
    day: "Saturday",
    date: "July 25",
    shows: [
      { artist: "Ari", venue: "The Cellar", time: "6pm" },
      { artist: "Charlee Prayers", venue: "M&J Tavern", time: "9pm" },
      { artist: "Cover Story", venue: "On Tap", time: "6pm" },
      { artist: "Coyote Rider", venue: "Worthy Brewing", time: "7pm" },
      { artist: "Eric Leadbetter", venue: "Stoller Wine Bar", time: "5pm" },
      { artist: "The Gibbons", venue: "Father Luke's Room", time: "7pm" },
      { artist: "The Happy's & Kimberly June", venue: "Silver Moon Brewing", time: "7pm" },
      { artist: "Jordan Wolfe", venue: "The Grove Market Hall", time: "6pm" },
      { artist: "Ledyard & Nick Campbell", venue: "Austin Kitchen Wine Bar & Mercantile", time: "5pm" },
      { artist: "Monkey Mode", venue: "Rivers Place Taphouse", time: "6pm" },
      { artist: "Parties Of Progress - Pink Party 2.0", venue: "Volcanic Theatre Pub", time: "8pm" },
      { artist: "Schaab & Sofie", venue: "Dogwood at The Pine Shed", time: "9pm" },
      { artist: "Small Town", venue: "Northside Bar & Grill", time: "8pm" },
      { artist: "Super Greens", venue: "The Commonwealth Pub", time: "8pm" },
      { artist: "Tony Smiley", venue: "Portello Wine Cafe", time: "7pm" },
    ],
  },
  {
    day: "Sunday",
    date: "July 26",
    shows: [
      { artist: "Blakkamoore w/ Yungg Trip, Jubba White, & Simmer Down Sound", venue: "Volcanic Theatre Pub", time: "8pm" },
      { artist: "Eric Leadbetter", venue: "10 Barrel West Side Pub", time: "5pm" },
      { artist: "Goo Goo Dolls w/ Neon Trees", venue: "Hayden Homes Amphitheater", time: "6:30pm" },
      { artist: "Heller Highwater Band", venue: "Ballers & Brews", time: "4pm" },
      { artist: "KC Flynn", venue: "Rivers Place Taphouse", time: "6pm" },
      { artist: "Kimberly June", venue: "Goodlife Brewing Company", time: "4pm" },
      { artist: "Kurt Silva & Cynthia West", venue: "Riverhouse Lodge", time: "11am" },
      { artist: "Long Gone Wilder", venue: "Deschutes Brewery Beer Garden", time: "4pm" },
      { artist: "Shine(ola) Sing Along", venue: "The Commonwealth Pub", time: "4pm" },
    ],
  },
];

// Highlights shown on the cover — update each week
const HIGHLIGHTS = [
  { artist: "Mari & The Dream", day: "Mon Jul 20" },
  { artist: "Jaws Of Brooklyn", day: "Tue Jul 21" },
  { artist: "Futurebirds", day: "Fri Jul 24" },
  { artist: "The Happys", day: "Sat Jul 25" },
  { artist: "Goo Goo Dolls", day: "Sun Jul 26" },
];
