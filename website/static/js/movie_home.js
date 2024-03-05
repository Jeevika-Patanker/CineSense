const slider = document.querySelector('.card-container');
const content = document.querySelector('.content');
const main = document.getElementById('click');
var ScrollPerClick;
var ImagePadding = 20;
var scrollAmount = 0;
const API_KEY = 'api_key=b2084cac0164f1d1fb47762399c270af'
// var genreListURL="https://api.themoviedb.org/3/genre/movie/list?"+API_KEY;
const BASE_URL = 'https://api.themoviedb.org/3';
const API_URL = BASE_URL + '/discover/movie?include_adult=false&sort_by=popularity.desc&'+API_KEY;
const IMG_URL = 'https://image.tmdb.org/t/p/w185';

    
    const genres = [
        {
            "id": 28,
            "name": "Action"
        },
        {
            "id": 12,
            "name": "Adventure"
        },
        {
            "id": 16,
            "name": "Animation"
        },
        {
            "id": 35,
            "name": "Comedy"
        },
        {
            "id": 80,
            "name": "Crime"
        },
        {
            "id": 99,
            "name": "Documentary"
        },
        {
            "id": 18,
            "name": "Drama"
        },
        {
            "id": 10751,
            "name": "Family"
        },
        {
            "id": 14,
            "name": "Fantasy"
        },
        {
            "id": 36,
            "name": "History"
        },
        {
            "id": 27,
            "name": "Horror"
        },
        {
            "id": 10402,
            "name": "Music"
        },
        {
            "id": 9648,
            "name": "Mystery"
        },
        {
            "id": 10749,
            "name": "Romance"
        },
        {
            "id": 878,
            "name": "Science Fiction"
        },
        {
            "id": 10770,
            "name": "TV Movie"
        },
        {
            "id": 53,
            "name": "Thriller"
        },
        {
            "id": 10752,
            "name": "War"
        },
        {
            "id": 37,
            "name": "Western"
        }]


showMovieData();



function SliderScrollLeft() {
    slider.scrollTo({
        top: 0,
        left: (scrollAmount -= ScrollPerClick),
        behaviour: "smooth"
    });

    if (scrollAmount < 0) {
        scrollAmount = 0;
    }
}
function SliderScrollRight() {

    if (scrollAmount <= slider.scrollWidth - slider.clientWidth) {
        slider.scrollTo({
            top: 0,
            left: (scrollAmount += ScrollPerClick),
            behaviour: "smooth"
        });
    }
}




async function showMovieData() {
    //fetching movie details here
    var result = await axios.get(API_URL) // to fetch movies data
    console.log(result);
    result = result.data.results;


    result.map(function (cur, index) {
        slider.insertAdjacentHTML(
            "beforeend",
            ` 
            <li class="card">
            <img src="https://image.tmdb.org/t/p/w185/${cur.poster_path}" class=" card-img img-${index}" alt="image-not-found" onclick="showDetails(${index})"/>
        </li>
             `
        )
        ScrollPerClick = 400
    })

}


async function showDetails(movieIndex) {
    console.log('INSIDE showDetails Function')
    let result = await axios.get(API_URL) // to fetch movies data
    result = result.data.results;
    const movie = result[movieIndex];


    if (movie) {
        genreNameList = []
        let title = movie.title;
        let overview = movie.overview;
        let release_date = movie.release_date;
        let id = movie.id;
        
        let backdrop_path = movie.backdrop_path;

        movie.genre_ids.forEach(element => {
            genre_name = getGenreNameById(element)
            genreNameList.push(genre_name);
        });

        // console.log(genreNameList)

        let spanContent = '';
        genreNameList.forEach(item => {
            spanContent += `<span>${item}</span>`;
        });

        console.log(spanContent)

        content.innerHTML = `
      <img src="https://image.tmdb.org/t/p/w185/${movie.poster_path}" alt="${title}" class="movie-title">
      <div class="active-details">
      <h3 class="carousel-title">${title}</h3>
      <h4> <span> Release Date: ${convertDateFormat(release_date)} </span></h4>
      <h4>
             
            `+ spanContent + `
          </h4>
          <p>${overview}</p>
          <div class="button-container">
              <a href='/current_screen?movieId=${id}&type=movie'><button>Watch</button></a>
              <a><button>Add to WatchList</button></a>
          </div>
      </div>
      
      `
      changeStyle(backdrop_path)
    }
}

function getGenreNameById(genreId) {
    const genre = genres.find(item => item.id === genreId);
    return genre ? genre.name : null;
}

function changeStyle(background) {
    main.style.background = "url('https://image.tmdb.org/t/p/original"+background+"') center center / cover";
}


function convertDateFormat(inputDate) {
    const months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ];

    const [year, month, day] = inputDate.split('-').map(Number);
    const monthName = months[month - 1];

    return `${day} ${monthName} ${year}`;
}










