function searchQuery(){
    var moviequery = $('#addmovie-field').val()
    //console.log(moviequery)
    $.post( '/searchmovie', { "query": moviequery } ).done(function(response) {
        //console.log(response['movies'])
        movies = response['movies']
        $('#search-results').html(movies);
    }).fail(function() {
        //
    });
}

function getvotes(movie_name,movie_row){
    $('.vote-row').remove();
    $.post( '/getvotes', { 'movie_name':movie_name } ).done(function(response) {
        console.log('Putting votes under: '+movie_row.attr('id'))
        votes_list = response['votes']
        if (votes_list.length != 0){
            //adds extra rows under the row that shows votes, only does this if the row is selected
            votes_list.forEach(vote => {
                if (movie_row.hasClass('selected-movie')){
                    movie_row.after(`
                    <tr class="vote-row" id="${movie_name}-vote-row-${vote}">
                        <td class="vote-row"></td>
                        <td class="vote-row"></td>
                        <td class="vote-row">${vote}</td>
                        <td class="vote-row"><span>+1</span></td>
                        <td class="vote-row"></td>
                    </tr>
                    `);
                }
            });
        }
    })
}

function getinfo(selected_movie,movie_row,refresh){
    console.log('Searching for a poster for: '+selected_movie)
    $('#poster-loading-icon').fadeIn();
    $.post( '/getinfo', { "query": selected_movie, "refresh":refresh } ).done(function(response) {
        console.log("Succeeded getting the poster");
        if (response['color'] == 'light'){
            $('.lds-ellipsis div').css('background','#000000')
        }else{
            $('.lds-ellipsis div').css('background','#fff')
        }
        
        poster_url = response['poster']
        movie_name = response['name']
        $('#poster-loading-icon').fadeOut();
        $('#movie-poster').css('background-image',`url(${poster_url})`)
        $('#movie-year').text(`${response['year']}`)
        $('#movie-rating').text(`${response['rating']}`)
        $('#movie-genres').text(`${response['genres']}`)
        $('#movie-director').text(`${response['director']}`)
        $('#movie-plot').text(`${response['plot']}`)
        //$('#movie-imdbpage').text(`${response['imdbpage']}`)
        $('#movie-imdbpage').html(`<a href="${response['imdbpage']}">Link</a>`)
        if(movie_name){
            getvotes(selected_movie,movie_row);
        }
        
        //$('#movie-info').fadeIn("fast");
    }).fail(function() {
        console.log("Failed getting the poster");
        $('#poster-loading-icon').fadeOut();
        $('#movie-poster').css('background-image',`url('/static/images/no-movie-poster.png')`)
        //$('#movie-info').fadeIn("fast");
    });
}


function sortmovies(){
    console.log('Sorting movies by vote')
    $table = $('#movie-que-table')
    $table.fadeOut('fast');
    $rows = $('tbody > tr', $table).not('#table-header');

    $rows.sort(function(a, b) {
        var keyA = $('td:last-child',a).find('span').text();
        var keyB = $('td:last-child',b).find('span').text();
        return (keyB > keyA) ? 1 : 0;  // A bigger than B, sorting ascending
    });

    $rows.each(function(index, row){
        $table.append(row);                  // append rows after sort
    });

    $table.fadeIn('fast');
}



