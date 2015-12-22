var gulp = require('gulp');
var sass = require('gulp-sass');
var watch = require('gulp-watch');
var minifyCss = require('gulp-minify-css');
var rename = require('gulp-rename');
var concat = require('gulp-concat');
var sourcemaps = require('gulp-sourcemaps');
var ngAnnotate = require('gulp-ng-annotate');
var bytediff = require('gulp-bytediff');
var uglify = require('gulp-uglify');
var plumber = require('gulp-plumber');
var jshint = require('gulp-jshint');
var jscs = require('gulp-jscs');

var sourcePath = './frontend_source/';
var pkg = {
      src: {
              base: sourcePath
            , sass: sourcePath + 'sass/**/*.sass'
            , modulesSass: sourcePath + 'apps/**/*.sass'
            , js: sourcePath + 'apps/**/!(*.specs).js'
            , angularModules: sourcePath + 'apps/**/*.module.js'
            , angularTemplates: sourcePath + 'apps/**/*.html'
            , images: sourcePath + 'images/**/*'
            , fonts: sourcePath + 'fonts/**/*'
        }
    , dest: './homesite/static/'
};

gulp.task('default', [
      'build'
    , 'watch'
]);

gulp.task('build', [
      'sass'
    , 'scripts'
    , 'images'
    , 'fonts'
]);

/**
 * Run sass
 */
gulp.task('sass', function (done) {
    gulp.src([
            pkg.src.modulesSass
            , pkg.src.base + 'sass/bundle.sass'
        ])
        .pipe(sass().on('error', sass.logError))
        .pipe(bytediff.start())
        .pipe(minifyCss({
            keepSpecialComments: 0
        }))
        .pipe(bytediff.stop())
        .pipe(concat('bundle.min.css'))
        .pipe(gulp.dest(pkg.dest + 'css/'))
        .on('end', done);
});

/**
 * Handle all JS compilation stuff
 */
gulp.task('scripts', function () {
    gulp.src([
              pkg.src.angularModules
            , pkg.src.js
        ])
        .pipe(plumber())
        .pipe(sourcemaps.init())
        .pipe(jscs({
            fix: false
            , configPath: '.jscsrc'
        }))
        .pipe(jscs.reporter())
        .pipe(jscs({
            fix: true
            , configPath: '.jscsrc-build'
        }))
        .pipe(jshint())
        .pipe(jshint.reporter('jshint-stylish'))
        .pipe(concat('bundle.min.js', {newLine: ';'}))
        .pipe(ngAnnotate({ add: true }))
        .pipe(bytediff.start())
        .pipe(uglify({mangle: true}))
        .pipe(bytediff.stop())
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest(pkg.dest + 'js/'));
    gulp.src(pkg.src.angularTemplates)
        .pipe(gulp.dest(pkg.dest + 'apps/'));
});

/**
 * Copy images
 */
gulp.task('images', function () {
    gulp.src(pkg.src.images)
        .pipe(gulp.dest(pkg.dest + 'images/'));
});

/**
 * Copy fonts
 */
gulp.task('fonts', function () {
    gulp.src(pkg.src.fonts)
        .pipe(gulp.dest(pkg.dest + 'fonts/'));
});

/**
 * Watch files for recompilation
 */
gulp.task('watch', function () {
    gulp.watch([pkg.src.sass, pkg.src.modulesSass], ['sass']);
    gulp.watch([
          pkg.src.js
        , pkg.src.angularTemplates
    ],                              ['scripts']);
    gulp.watch([pkg.src.images],    ['images']);
    gulp.watch([pkg.src.fonts],     ['fonts']);
});