// ─────────────────────────────────────────────
// BANDS IN BEND — Weekly Show Data
// Update this file each week to refresh the site
// ─────────────────────────────────────────────

const WEEK = {
  label: "August 10 – 16",
  year: "2026",
};

const SHOWS = [
  {
    day: "Monday",
    date: "August 10",
    shows: [
      { artist: "Bluegrass Collective", venue: "Silver Moon Brewing", time: "6pm" },
      { artist: "Musicians Open Showcase", venue: "The Commonwealth Pub", time: "5pm" },
      { artist: "Sun Threaders", venue: "On Tap", time: "6pm" },
      { artist: "Weekly Live Music", venue: "Bend Brewing Company", time: "6pm" },
    ],
  },
  {
    day: "Tuesday",
    date: "August 11",
    shows: [
      { artist: "Chris Baron", venue: "Silver Moon Brewing", time: "6pm" },
      { artist: "Mari & The Dream", venue: "Goodlife Brewing Company", time: "6pm" },
      { artist: "Penny & Sparrow w/ Cece Coakley", venue: "Volcanic Theatre Pub", time: "7pm" },
      { artist: "T5 Jazz", venue: "The Commonwealth Pub", time: "7pm" },
      { artist: "Vern Johnson", venue: "Deschutes Brewery Beer Garden", time: "5pm" },
      { artist: "Weekly Live Music", venue: "Greg's Grill", time: "6pm" },
    ],
  },
  {
    day: "Wednesday",
    date: "August 12",
    shows: [
      { artist: "Acoustic Open Mic w/ Derek Michael Marc", venue: "Northside Bar & Grill", time: "6pm" },
      { artist: "Daring Greatly", venue: "The Commonwealth Pub", time: "8pm" },
      { artist: "Dumpster Joe", venue: "Father Luke's Room", time: "7pm" },
      { artist: "Erin Cole-Baker", venue: "Crosscut Warming Hut No. 5", time: "6pm" },
      { artist: "Joyful Lane", venue: "Austin Kitchen Wine Bar & Mercantile", time: "5pm" },
      { artist: "Kristen Ford", venue: "Silver Moon Brewing", time: "7pm" },
      { artist: "Long Gone Wilder", venue: "Tetherow Resort", time: "5pm" },
      { artist: "Ol' Time Music w/ Danger Gently & Friends", venue: "The Cellar", time: "6pm" },
      { artist: "STS9 Human Dream Tour", venue: "Midtown Ballroom", time: "8pm" },
    ],
  },
  {
    day: "Thursday",
    date: "August 13",
    shows: [
      { artist: "Anderson Koenig", venue: "Austin Kitchen Wine Bar & Mercantile", time: "5pm" },
      { artist: "Broken Charley", venue: "Worthy Brewing", time: "5pm" },
      { artist: "Coyote Rider", venue: "Stoller Wine Bar", time: "6pm" },
      { artist: "The Critical Blues Band", venue: "Bevel Craft Brewing", time: "6pm" },
      { artist: "The Cutman", venue: "The Commonwealth Pub", time: "7:30pm" },
      { artist: "Dark and Grey", venue: "Northside Bar & Grill", time: "7pm" },
      { artist: "Irish Traditional Music", venue: "The Cellar", time: "6pm" },
      { artist: "Mari & The Dream", venue: "Mountain Burger", time: "6pm" },
      { artist: "Papa Echo w/ Annika Hankshaw", venue: "M&J Tavern", time: "9pm" },
      { artist: "Rusty McRae", venue: "The Lot", time: "6pm" },
      { artist: "Sonic Benders", venue: "Silver Moon Brewing", time: "6pm" },
      { artist: "Sweet Motor", venue: "Rivers Place Taphouse", time: "6pm" },
      { artist: "Vinyl Night", venue: "Dogwood at The Pine Shed", time: "7pm" },
    ],
  },
  {
    day: "Friday",
    date: "August 14",
    shows: [
      { artist: "The ABluestics", venue: "Currents at Riverhouse Lodge", time: "7pm" },
      { artist: "Almost", venue: "Boneyard Pub", time: "6pm" },
      { artist: "Cheyenne West", venue: "Portello Lounge", time: "6:30pm" },
      { artist: "DJ ALXM", venue: "The Coyote", time: "9pm" },
      { artist: "Double Jump", venue: "The Grove Market Hall", time: "6pm" },
      { artist: "Dry Canyon Stampede", venue: "The Commonwealth Pub", time: "8pm" },
      { artist: "Jackrat, Sungrater, & Long Operators", venue: "M&J Tavern", time: "9pm" },
      { artist: "Jampoke", venue: "Silver Moon Brewing", time: "7pm" },
      { artist: "Larches & Mari And The Dream", venue: "Silver Moon Brewing", time: "7pm" },
      { artist: "Los Chavalones Tour 2026, Los DOs de Tamaulipas", venue: "Midtown Ballroom", time: "8pm" },
      { artist: "Mighty Moves", venue: "Dogwood at The Pine Shed", time: "8pm" },
      { artist: "Sleepless Truckers", venue: "Worthy Brewing", time: "7pm" },
      { artist: "Ty Myers w/ Brent Cobb & Benny G", venue: "Hayden Homes Amphitheater", time: "6:30pm" },
      { artist: "Van Death", venue: "The Cellar", time: "6pm" },
      { artist: "Ying Yang Twins & MIMS 2000s Throwback Party", venue: "Silver Moon Brewing", time: "7pm" },
    ],
  },
  {
    day: "Saturday",
    date: "August 15",
    shows: [
      { artist: "Chris Beland", venue: "Portello Lounge", time: "6:30pm" },
      { artist: "Dirty Nature & Greg Garretson", venue: "The Capitol", time: "5:30pm" },
      { artist: "DJ ALXM", venue: "The Coyote", time: "9pm" },
      { artist: "DJ Mark Brody", venue: "Dogwood at The Pine Shed", time: "9pm" },
      { artist: "Doc Ryan Band", venue: "On Tap", time: "6pm" },
      { artist: "Double Jump", venue: "The Commonwealth Pub", time: "8pm" },
      { artist: "Dustin Nagy", venue: "Stoller Wine Bar", time: "5pm" },
      { artist: "Festival Orchestra: John Williams & The American Journey", venue: "Tower Theatre", time: "7:30pm" },
      { artist: "Goth Babe & JW Francis", venue: "Silver Moon Brewing", time: "7pm" },
      { artist: "Mighty Moves", venue: "The Canteen at Campfire Hotel", time: "3pm" },
      { artist: "Mustang County Boxing Jamboree", venue: "Wandering Ranchero", time: "7pm" },
      { artist: "O.A.R. w/ Gavin Degraw & Lisa Loeb", venue: "Hayden Homes Amphitheater", time: "5:30pm" },
      { artist: "Robot Mushroom", venue: "The Cellar", time: "6pm" },
      { artist: "Rubbah Tree", venue: "Worthy Brewing", time: "7pm" },
      { artist: "Sagebrush", venue: "Northside Bar & Grill", time: "8pm" },
      { artist: "Sugar Mountain", venue: "Austin Kitchen Wine Bar & Mercantile", time: "5pm" },
      { artist: "The Uncharted Project", venue: "The Grove Market Hall", time: "6pm" },
    ],
  },
  {
    day: "Sunday",
    date: "August 16",
    shows: [
      { artist: "Almost", venue: "Ballers & Brews", time: "4pm" },
      { artist: "Belltower Band", venue: "Goodlife Brewing Company", time: "4pm" },
      { artist: "Fluffalove", venue: "Deschutes Brewery Beer Garden", time: "4pm" },
      { artist: "GBots", venue: "Midtown Yacht Club", time: "6pm" },
      { artist: "Magnolia Boulevard", venue: "Silver Moon Brewing", time: "6pm" },
      { artist: "Mark Ransom & Pat Pearsall", venue: "10 Barrel West Side Pub", time: "5pm" },
      { artist: "Mr. Danimals, Giancarlo & Friends", venue: "The Canteen at Campfire Hotel", time: "3pm" },
      { artist: "Trifecta - Celtic Music", venue: "The Commonwealth Pub", time: "4pm" },
      { artist: "The Uncharted Project", venue: "Currents at Riverhouse Lodge", time: "11am" },
    ],
  },
];

// Highlights shown on the cover — update each week
const HIGHLIGHTS = [
  { artist: "Penny & Sparrow", day: "Tue Aug 11" },
  { artist: "STS9", day: "Wed Aug 12" },
  { artist: "Jampoke", day: "Fri Aug 14" },
  { artist: "Goth Babe", day: "Sat Aug 15" },
  { artist: "Magnolia Boulevard", day: "Sun Aug 16" },
];
