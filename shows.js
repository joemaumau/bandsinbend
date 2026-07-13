// ─────────────────────────────────────────────
// BANDS IN BEND — Weekly Show Data
// Update this file each week to refresh the site
// ─────────────────────────────────────────────

const WEEK = {
  label: "July 13 – 19",
  year: "2026",
};

const SHOWS = [
  {
    day: "Monday",
    date: "July 13",
    shows: [
      { artist: "Bluegrass Collective", venue: "Silver Moon Brewing", time: "6pm" },
      { artist: "Massdead & Infuriate", venue: "The Domino Room", time: "7pm" },
      { artist: "Sakoyana", venue: "On Tap", time: "6pm" },
    ],
  },
  {
    day: "Tuesday",
    date: "July 14",
    shows: [
      { artist: "Jazzbos", venue: "The Commonwealth Pub", time: "7pm" },
      { artist: "Popcorn Trio", venue: "Goodlife Brewing Company", time: "6pm" },
      { artist: "Sakoyana", venue: "Silver Moon Brewing", time: "7pm" },
      { artist: "Shinyribs & Schaefer Llana", venue: "The Domino Room", time: "7pm" },
      { artist: "Two Crows For Comfort", venue: "Silver Moon Brewing", time: "6:30pm" },
      { artist: "Vern Johnson & Friends", venue: "Deschutes Brewery Beer Garden", time: "7pm" },
    ],
  },
  {
    day: "Wednesday",
    date: "July 15",
    shows: [
      { artist: "Chasing Ebenezer", venue: "The Commonwealth Pub", time: "7:30pm" },
      { artist: "Kenny Hadden w/ Casey Willis", venue: "Crosscut Warming Hut No. 5", time: "6pm" },
      { artist: "Long Gone Wilder", venue: "Austin Kitchen Wine Bar & Mercantile", time: "5pm" },
      { artist: "Mavis & Bretz", venue: "Father Luke's Room", time: "7pm" },
      { artist: "Sam Barber w/ John Vincent III & Wild Horses", venue: "Hayden Homes Amphitheater", time: "6:30pm" },
      { artist: "Seamus O'Sullivan", venue: "Tetherow Resort", time: "5pm" },
      { artist: "Warsaw Poland Bros. w/ Micah Schnabel & Vanessa Jean Speckman", venue: "Silver Moon Brewing", time: "7pm" },
    ],
  },
  {
    day: "Thursday",
    date: "July 16",
    shows: [
      { artist: "Andre Nickatina", venue: "Silver Moon Brewing", time: "8pm" },
      { artist: "Beverly Anderson", venue: "Portello Wine Cafe", time: "6:30pm" },
      { artist: "Bill Powers Old Growth", venue: "Rivers Place Taphouse", time: "6pm" },
      { artist: "Carson Hackbart", venue: "The Coyote", time: "5pm" },
      { artist: "Charley Crockett w/ Margo Price", venue: "Hayden Homes Amphitheater", time: "6:30pm" },
      { artist: "Coyote Rider", venue: "Stoller Wine Bar", time: "6pm" },
      { artist: "Draven Schmidt", venue: "The Lot", time: "6pm" },
      { artist: "For Now, Yeah!", venue: "M&J Tavern", time: "9pm" },
      { artist: "Garrett & Ollie", venue: "Austin Kitchen Wine Bar & Mercantile", time: "5pm" },
      { artist: "Leftover Salmon w/ Kota Dosa", venue: "Drake Park Munch & Music", time: "5:30pm" },
      { artist: "Mark Creech", venue: "The Grove Market Hall", time: "6pm" },
      { artist: "Nick Lutsko & $100K Band", venue: "Volcanic Theatre Pub", time: "7pm" },
      { artist: "Sakoyana", venue: "The Commonwealth Pub", time: "7:30pm" },
      { artist: "Summit Express Jazz Band", venue: "Bevel Craft Brewing", time: "6pm" },
      { artist: "Victor Johnson", venue: "Mountain Burger", time: "6pm" },
    ],
  },
  {
    day: "Friday",
    date: "July 17",
    shows: [
      { artist: "Adam Gabriel", venue: "Riverhouse Lodge", time: "7pm" },
      { artist: "Big Treble", venue: "M&J Tavern", time: "9pm" },
      { artist: "Chasing Ebenezer", venue: "Father Luke's Room", time: "7pm" },
      { artist: "Future Joy", venue: "Silver Moon Brewing", time: "7pm" },
      { artist: "Good Trouble", venue: "The Commonwealth Pub", time: "8pm" },
      { artist: "Jimmy Eat World w/ Motion City Soundtrack // Illuminati Hotties", venue: "Hayden Homes Amphitheater", time: "6pm" },
      { artist: "Jordan Wolfe", venue: "Portello Wine Cafe", time: "6:30pm" },
      { artist: "Jupiter Williams", venue: "Dogwood at The Pine Shed", time: "9pm" },
      { artist: "Mickey Avalon w/ Joe C Note & The Hobbyist", venue: "Volcanic Theatre Pub", time: "7pm" },
      { artist: "Nicholas Fennel", venue: "The Cellar", time: "6pm" },
      { artist: "Party in the Back", venue: "Worthy Brewing", time: "7pm" },
      { artist: "Pendleton Highway", venue: "Boneyard Pub", time: "6pm" },
      { artist: "Wic Whitney & Zac Loyd", venue: "Silver Moon Brewing", time: "7pm" },
    ],
  },
  {
    day: "Saturday",
    date: "July 18",
    shows: [
      { artist: "Caveman Dave", venue: "The Grove Market Hall", time: "6pm" },
      { artist: "Cecilia Voss", venue: "The Cellar", time: "6pm" },
      { artist: "Club Reggaeton w/ DJ Mistico, DJ Cruz, & DJ EMVY", venue: "Midtown Ballroom", time: "10pm" },
      { artist: "DuBb Central", venue: "On Tap", time: "6pm" },
      { artist: "Eric Leadbetter Band", venue: "Worthy Brewing", time: "7pm" },
      { artist: "Johnny Bourbon", venue: "Wandering Ranchero", time: "7pm" },
      { artist: "JuJu Eyeball", venue: "The Commonwealth Pub", time: "8pm" },
      { artist: "Kota Dosa", venue: "Silver Moon Brewing", time: "7pm" },
      { artist: "The Kronk Men w/ Weapon World & Herb", venue: "M&J Tavern", time: "9pm" },
      { artist: "Levity & Tape B w/ Canabliss", venue: "Hayden Homes Amphitheater", time: "6pm" },
      { artist: "Long Gone Wilder w/ Rachel Fishman", venue: "Portello Wine Cafe", time: "6:30pm" },
      { artist: "Mark Creech", venue: "Stoller Wine Bar", time: "5pm" },
      { artist: "Matt Wax B2B Welterweight, Shalyssa B2B Ground$core & Eyeneye B2B Swelltimes", venue: "Volcanic Theatre Pub", time: "10pm" },
      { artist: "Sleaze", venue: "Dogwood at The Pine Shed", time: "9pm" },
      { artist: "So Much House w/ Furtha, Liamlantern, Wookstarz, & Skora", venue: "Silver Moon Brewing", time: "10pm" },
      { artist: "Sugar Mountain", venue: "Austin Kitchen Wine Bar & Mercantile", time: "5pm" },
    ],
  },
  {
    day: "Sunday",
    date: "July 19",
    shows: [
      { artist: "The Abluestics", venue: "Deschutes Brewery Beer Garden", time: "4pm" },
      { artist: "Carson Hackbart", venue: "Riverhouse Lodge", time: "11am" },
      { artist: "Garret T. Willie", venue: "Silver Moon Brewing", time: "6pm" },
      { artist: "Mavis Bretz", venue: "10 Barrel West Side Pub", time: "5pm" },
      { artist: "Molly Moons", venue: "Ballers & Brews", time: "4pm" },
      { artist: "Pete Kartsounes", venue: "Goodlife Brewing Company", time: "4pm" },
      { artist: "Red Red", venue: "Midtown Yacht Club", time: "6pm" },
      { artist: "Serpentfoot w/ Milk for the Angry Sungrater", venue: "Volcanic Theatre Pub", time: "6pm" },
      { artist: "Shine(ola) Sing Along", venue: "The Commonwealth Pub", time: "8pm" },
    ],
  },
];

// Highlights shown on the cover — update each week
const HIGHLIGHTS = [
  { artist: "Vern Johnson", day: "Tue Jul 14" },
  { artist: "Sam Barber", day: "Wed Jul 15" },
  { artist: "Charley Crockett", day: "Thu Jul 16" },
  { artist: "Jimmy Eat World", day: "Fri Jul 17" },
  { artist: "Kota Dosa", day: "Sat Jul 18" },
];
