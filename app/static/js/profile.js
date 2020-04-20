function selectmovie(movie_row){
    console.log(`Selecting movie ${$(movie_row).attr('id')}`);
    $('.selected-movie').removeClass('selected-movie');
    $(movie_row).addClass('selected-movie');
    //getinfo($(movie_row).attr('id'),$(movie_row),refresh=false);
    //$(movie_row).find('td:first-child').find('.delete_button').fadeIn()
}