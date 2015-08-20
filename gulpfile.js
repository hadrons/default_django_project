var gulp = require('gulp');
var sass = require('gulp-sass');
var watch = require('gulp-watch');
var minifyCss = require('gulp-minify-css');
var rename = require('gulp-rename');

gulp.task('default', ['sass', 'watch']);

var root = 'homesite/static';

gulp.task('sass', function (done) {
    gulp.src(root+'/sass/comum.sass')
        .pipe(sass().on('error', sass.logError))
        .pipe(gulp.dest(root+'/css/'))
        .pipe(minifyCss({
            keepSpecialComments: 0
        }))
        .pipe(rename({
            extname: '.min.css'
        }))
        .pipe(gulp.dest(root+'/css/'))
        .on('end', done);
});

gulp.task('watch', function () {
    gulp.watch([root+'/sass/**/*.sass'], ['sass']);
});
