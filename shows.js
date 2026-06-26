// ─────────────────────────────────────────────
// BANDS IN BEND — Weekly Show Data
// Update this file each week to refresh the site
// ─────────────────────────────────────────────

const WEEK = {
  label: "June 25 – July 5",
  year: "2026",
};

const SHOWS = [
  {
    day: "Thursday",
    date: "June 25",
    shows: [
      { artist: "BendreTheGiant w/ Palo Soprano", venue: "The Commonwealth Pub", time: "7:30pm" },
      { artist: "Larkspur Stand", venue: "Rivers Place Taphouse", time: "6pm" },
      { artist: "Scott Pemberton", venue: "Worthy Brewing", time: "7pm" },
      { artist: "Souljers Rising", venue: "Bevel Craft Brewing", time: "6pm" },
    ],
  },
  {
    day: "Friday",
    date: "June 26",
    shows: [
      { artist: "DJ Timothy Bee", venue: "Dogwood at the Pine Shed", time: "9pm" },
      { artist: "Eric Leadbetter", venue: "Northside Bar & Grill", time: "6pm" },
      { artist: "KPOV Beatles Sing Along", venue: "The Commonwealth Pub", time: "7pm" },
      { artist: "Parker McCollum w/ Vincent Mason, Aubrie Sellers", venue: "Hayden Homes Amphitheater", time: "6:30pm" },
      { artist: "Party in the Back", venue: "Worthy Brewing", time: "7pm" },
      { artist: "Surf Hat", venue: "Domino Room", time: "7pm" },
      { artist: "The Chilling Alpine Adventure", venue: "Silver Moon", time: "7pm" },
    ],
  },
  {
    day: "Saturday",
    date: "June 27",
    shows: [
      { artist: "Bend Blues Fest", venue: "Silver Moon", time: "12pm" },
      { artist: "Chris Beland", venue: "On Tap", time: "6pm" },
      { artist: "Dizgo & Mamasboy", venue: "The Domino Room", time: "8pm" },
      { artist: "Dry Canyon Stampede", venue: "Worthy Brewing", time: "7pm" },
      { artist: "Lonnie Mardis Quartet", venue: "Rivers Place Taphouse", time: "6pm" },
      { artist: "Megan Diana", venue: "Father Luke's Room", time: "7pm" },
      { artist: "Rhiannon Giddens w/ Mary Chapin Carpenter, Mavis Staples, Hurray For The Riff Raff", venue: "Hayden Homes Amphitheater", time: "6pm" },
      { artist: "Sagebrush Rock", venue: "Northside Bar & Grill", time: "8pm" },
      { artist: "Schab + Sofie", venue: "Dogwood at the Pine Shed", time: "9pm" },
      { artist: "The Substitutes", venue: "The Commonwealth Pub", time: "8pm" },
      { artist: "Switchback", venue: "M&J Tavern", time: "9pm" },
    ],
  },
  {
    day: "Sunday",
    date: "June 28",
    shows: [
      { artist: "High Fade w/ Brass Camel", venue: "Volcanic Theater Courtyard", time: "7pm" },
      { artist: "Shineola Sing Along", venue: "The Commonwealth Pub", time: "4pm" },
    ],
  },
  {
    day: "Monday",
    date: "June 29",
    shows: [
      { artist: "Bluegrass Collective", venue: "Silver Moon", time: "6pm" },
      { artist: "Bong Wizard, Sandkrawler, Vacancy Floor, & James G", venue: "The Domino Room", time: "8:30pm" },
    ],
  },
  {
    day: "Tuesday",
    date: "June 30",
    shows: [
      { artist: "Goldpine", venue: "Silver Moon Brewing", time: "6:30pm" },
      { artist: "Open Jam by Mari", venue: "Silver Moon Brewing", time: "7pm" },
      { artist: "Sean Alan & Jazz On the Side", venue: "The Commonwealth Pub", time: "7pm" },
    ],
  },
  {
    day: "Wednesday",
    date: "July 1",
    shows: [
      { artist: "Amelia Day", venue: "Silver Moon Brewing", time: "7pm" },
      { artist: "Brent Alan & Brother Gabe Duo", venue: "Father Luke's Room", time: "7pm" },
      { artist: "Eric Leadbetter", venue: "Tetherow Resort", time: "5pm" },
      { artist: "Kurt Silva and Cynthia West", venue: "The Commonwealth Pub", time: "7:30pm" },
    ],
  },
  {
    day: "Thursday",
    date: "July 2",
    shows: [
      { artist: "Blackstrap Bluegrass", venue: "Rivers Place Taphouse", time: "6pm" },
      { artist: "Broken Top Bluegrass", venue: "Bevel Brewing Company", time: "6pm" },
      { artist: "Cherry: A Perfect Vinyl Night w/ DJ Timothy Bee", venue: "Dogwood at The Pine Shed", time: "7pm" },
      { artist: "Gabriel Cox Band", venue: "Silver Moon Brewing", time: "7pm" },
      { artist: "Moontricks w/ Mamas Boy", venue: "Drake Park Munch & Music", time: "5:30pm" },
      { artist: "Talamh Dubh", venue: "The Commonwealth Pub", time: "6:30pm" },
      { artist: "Traditional Irish Music", venue: "The Cellar", time: "6pm" },
    ],
  },
  {
    day: "Friday",
    date: "July 3",
    shows: [
      { artist: "Band of Comerados", venue: "Silver Moon Brewing", time: "7pm" },
      { artist: "Chris Beland", venue: "Father Luke's Room", time: "7pm" },
      { artist: "G-Bots & The Journeymen", venue: "The Commons Cafe & Taproom", time: "6:30pm" },
      { artist: "Rambler Kane", venue: "On Tap", time: "6pm" },
      { artist: "Smoker Dad & Family Worship Center", venue: "Silver Moon Brewing", time: "7pm" },
      { artist: "Soul’d Out", venue: "The Commonwealth Pub", time: "6:30pm" },
      { artist: "Travis Ehrenstrom", venue: "Worthy Brewing", time: "7pm" },
    ],
  },
  {
    day: "Saturday",
    date: "July 4",
    shows: [
      { artist: "Brent Alan & His Funky Friends", venue: "On Tap", time: "8pm" },
      { artist: "Call Down Thunder", venue: "Silver Moon Brewing", time: "6pm" },
      { artist: "JuJu Eyeball – Fourth of July Party", venue: "The Commonwealth Pub", time: "7pm" },
      { artist: "Midnight Cove", venue: "On Tap", time: "5pm" },
    ],
  },
  {
    day: "Sunday",
    date: "July 5",
    shows: [
      { artist: "Bong Wizard, Sandkrawler, Vacancy Floor, & James G", venue: "The Domino Room", time: "8:30pm" },
      { artist: "Eric Leadbetter & Pete Kartsounes", venue: "Rivers Place Taphouse", time: "6pm" },
    ],
  },
];

// Highlights shown on the cover — update each week
const HIGHLIGHTS = [
  { artist: "Goldpine", day: "Tue Jun 30" },
  { artist: "Amelia Day", day: "Wed Jul 1" },
  { artist: "Moontricks", day: "Thu Jul 2" },
  { artist: "Rambler Kane", day: "Fri Jul 3" },
  { artist: "Juju Eyeball", day: "Sat Jul 4" },
];
