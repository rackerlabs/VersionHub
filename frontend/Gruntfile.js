/* jslint node: true */
// TODO send report to file

// Generated on 2013-08-17 using generator-angular 0.3.1
'use strict';
var LIVERELOAD_PORT = 35729;
var lrSnippet = require('connect-livereload')({
    port: LIVERELOAD_PORT
});
var mountFolder = function(connect, dir) {
    return connect.static(require('path').resolve(dir));
};

// # Globbing
// for performance reasons we're only matching one level down:
// 'test/spec/{,*/}*.js'
// use this if you want to recursively match all subfolders:
// 'test/spec/**/*.js'

module.exports = function(grunt) {
    // load all grunt tasks
    require('matchdep').filterDev('grunt-*').forEach(grunt.loadNpmTasks);

    var proxySnippet = require('grunt-connect-proxy/lib/utils').proxyRequest;

    // configurable paths
    var yeomanConfig = {
        app: 'app',
        dist: 'dist'
    };

    try {
        yeomanConfig.app = require('./bower.json').appPath || yeomanConfig.app;
    } catch (e) {}

    grunt.initConfig({
        yeoman: yeomanConfig,
        watch: {
            options: {
                livereload: LIVERELOAD_PORT
            },
            livereload: {
                files: [
                    '<%= yeoman.app %>/{,*/}*.html',
                    '{.tmp,<%= yeoman.app %>}/test/{,*/}*.js',
                    '{.tmp,<%= yeoman.app %>}/styles/{,*/}*.css',
                    '<%= yeoman.app %>/images/{,*/}*.{png,jpg,jpeg,gif,webp,svg}'
                ]
            },
            less: {
                files: ['{.tmp,<%= yeoman.app %>}/styles/{,*/}*.less'],
                tasks: ['less']
            },
            docs: {
                files: [ '{.tmp,<%= yeoman.app %>}/scripts/{,*/}*.js'],
                tasks: ['ngdocs']
            }
        },
        // 'less'-task configuration
        less: {
            // production config is also available
            development: {
                options: {
                    // Specifies directories to scan for @import directives when parsing.
                    // Default value is the directory of the source, which is probably what you want.
                    paths: ['{.tmp,<%= yeoman.app %>}/styles/']
                },
                files: {
                    // compilation.css  :  source.less
                    '<%= yeoman.app %>/styles/app.css': '{.tmp,<%= yeoman.app %>}/styles/app.less'
                }
            }
        },
        connect: {
            options: {
                port: 9000,
                // Change this to '0.0.0.0' to access the server from outside.
                hostname: 'localhost'
            },
            proxies: [
                {
                    context: '/api',
                    host: '10.14.211.159',
                    port: 8000,
                    https: false,
                    changeOrigin: false,
                    rewrite: {
                        '^/api': ''
                    }
                }
            ],
            livereload: {
                options: {
                    middleware: function(connect) {
                        return [
                            lrSnippet,
                            mountFolder(connect, '.tmp'),
                            mountFolder(connect, yeomanConfig.app),
                            proxySnippet
                        ];
                    }
                }
            },
            test: {
                options: {
                    middleware: function(connect) {
                        return [
                            lrSnippet,
                            mountFolder(connect, '.tmp'),
                            mountFolder(connect, yeomanConfig.app),
                            mountFolder(connect, 'test'),
                            proxySnippet
                        ];
                    }
                }
            },
            dist: {
                options: {
                    middleware: function(connect) {
                        return [
                            mountFolder(connect, yeomanConfig.dist)
                        ];
                    }
                }
            }
        },
        open: {
            server: {
                url: 'http://localhost:<%= connect.options.port %>'
            }
        },
        clean: {
            dist: {
                files: [{
                    dot: true,
                    src: [
                        '.tmp',
                        '<%= yeoman.dist %>/*',
                        '!<%= yeoman.dist %>/.git*'
                    ]
                }]
            },
            server: '.tmp'
        },
        stubby: {
            stubsServer: {
                // note the array collection instead of an object
                options: {
                    stubs: 3000
                },
                files: [{
                    src: [ 'test/api-mocks/*.yaml' ]
                }]
            }
        },
        jshint: {
            options: {
                jshintrc: '.jshintrc',
                ignores: ['<%= yeoman.app %>/scripts/lib/{,*/}*.js']
            },
            all: [
                'Gruntfile.js',
                '<%= yeoman.app %>/scripts/{,*/}*.js'
            ]
        },
        // not used since Uglify task does concat,
        // but still available if needed
        /*concat: {
          dist: {}
        },*/
        rev: {
            dist: {
                files: {
                    src: [
                        '<%= yeoman.dist %>/scripts/{,*/}*.js',
                        '<%= yeoman.dist %>/styles/{,*/}*.css',
                        '<%= yeoman.dist %>/images/{,*/}*.{png,jpg,jpeg,gif,webp,svg}',
                        '<%= yeoman.dist %>/styles/fonts/*'
                    ]
                }
            }
        },
        useminPrepare: {
            html: '<%= yeoman.app %>/index.html',
            options: {
                dest: '<%= yeoman.dist %>'
            }
        },
        usemin: {
            html: ['<%= yeoman.dist %>/{,*/}*.html'],
            css: ['<%= yeoman.dist %>/styles/{,*/}*.css'],
            options: {
                dirs: ['<%= yeoman.dist %>']
            }
        },
        imagemin: {
            dist: {
                files: [{
                    expand: true,
                    cwd: '<%= yeoman.app %>/images',
                    src: '{,*/}*.{png,jpg,jpeg}',
                    dest: '<%= yeoman.dist %>/images'
                }]
            }
        },
        svgmin: {
            dist: {
                files: [{
                    expand: true,
                    cwd: '<%= yeoman.app %>/images',
                    src: '{,*/}*.svg',
                    dest: '<%= yeoman.dist %>/images'
                }]
            }
        },
        cssmin: {
            // By default, your `index.html` <!-- Usemin Block --> will take care of
            // minification. This option is pre-configured if you do not wish to use
            // Usemin blocks.
            // dist: {
            //   files: {
            //     '<%= yeoman.dist %>/styles/main.css': [
            //       '.tmp/styles/{,*/}*.css',
            //       '<%= yeoman.app %>/styles/{,*/}*.css'
            //     ]
            //   }
            // }
        },
        htmlmin: {
            dist: {
                options: {
                    /*removeCommentsFromCDATA: true,
                      // https://github.com/yeoman/grunt-usemin/issues/44
                      //collapseWhitespace: true,
                      collapseBooleanAttributes: true,
                      removeAttributeQuotes: true,
                      removeRedundantAttributes: true,
                      useShortDoctype: true,
                      removeEmptyAttributes: true,
                      removeOptionalTags: true*/
                },
                files: [{
                    expand: true,
                    cwd: '<%= yeoman.app %>',
                    src: ['*.html', 'views/**/*.html', 'widgets/*.html', 'modules/**/*.html'],
                    dest: '<%= yeoman.dist %>'
                }]
            }
        },
        // Put files not handled in other tasks here
        copy: {
            dist: {
                files: [{
                    expand: true,
                    dot: true,
                    cwd: '<%= yeoman.app %>',
                    dest: '<%= yeoman.dist %>',
                    src: [
                        '*.{ico,png,txt}',
                        '.htaccess',
                        'images/{,*/}*.{gif,webp}',
                        'fonts/*',
                    ]
                }, {
                    expand: true,
                    cwd: '.tmp/images',
                    dest: '<%= yeoman.dist %>/images',
                    src: [
                        'generated/*'
                    ]
                }, {
                    expand: true,
                    cwd: 'ngdocs',
                    dest: '<%= yeoman.dist %>/ngdocs',
                    src: [
                        '**'
                    ]
                }
                ]
            }
        },
        concurrent: {
            server: [
                'jshint'
            ],
            test: [],
            dist: [
                'imagemin',
                'svgmin',
                'htmlmin'
            ]
        },
        karma: {
            options: {
                configFile: 'karma.conf.js',
            },
            dev: {
                singleRun: false
            },
            single: {
                singleRun: true
            },
            full: {
                singleRun: true,
                browsers: ['PhantomJS', 'Chrome', 'ChromeCanary', 'Firefox', 'Safari']
            }
        },
        // simplemocha: {
        //     options: {
        //         globals: ['expect'],
        //         timeout: 10000,
        //         ignoreLeaks: false,
        //         ui: 'bdd',
        //         reporter: 'nyan'
        //     },

        //     all: {
        //         src: ['test/**/*.func.js']
        //     }
        // },
        shell: {
            protractor: {
                options: {
                    stdout: true
                },
                command: function (file) {
                    var cmd = 'protractor test/protractor.conf.js';

                    if (typeof file !== 'undefined' && file.length > 0) {
                        cmd += ' --specs ' + file;
                    }

                    return cmd;
                }
            }
        },
        cdnify: {
            dist: {
                html: ['<%= yeoman.dist %>/*.html']
            }
        },
        ngmin: {
            dist: {
                files: [{
                    expand: true,
                    cwd: '<%= yeoman.dist %>/scripts',
                    src: '*.js',
                    dest: '<%= yeoman.dist %>/scripts'
                }]
            }
        },
        uglify: {
            dist: {
                files: {
                    '<%= yeoman.dist %>/scripts/scripts.js': [
                        '<%= yeoman.dist %>/scripts/scripts.js'
                    ]
                }
            }
        },
        plato: {
            default: {
                options: {
                    jshint: grunt.file.readJSON('.jshintrc'),
                    exclude: /app\/scripts\/lib/ // excludes files in lib directory
                },
                files: {
                    'report': ['app/scripts/**/*.js']
                }
            }
        },
        ngdocs: {
            options: {
                'dest': 'ngdocs',
                'title': 'Encore Developer Documentation',
                'html5Mode': false
            },
            all: ['app/scripts/**/*.js', 'test/browser-helpers.js']
        },
        styleguide: {
            options: {
                _: ['<%= yeoman.app %>/styles'],
                name: 'Encore',
                out: 'styleguide',
                in : ['<%= yeoman.app %>/styles'],
                include: [undefined],
                basePath: '<%= yeoman.app %>/styles'
            }
        }
    });

    // TODO
    grunt.registerTask('styleguide', function () {
        grunt.log.writeln('Generating CSS style guide');

        this.async();

        var styledocco = require('./node_modules/styledocco/cli.js');

        styledocco(this.options());
    });

    /* Usage: `$ grunt server` or `$ grunt server:dist` or `$ grunt server:stubbed:watch` */
    grunt.registerTask('server', function(target, watch) {
        var commonTasks = [
            'less',
            'clean:server',
            'configureProxies',
            'concurrent:server',
            'connect:livereload'
        ];

        if (target === 'dist') {
            return grunt.task.run(['build', 'open', 'connect:dist:keepalive']);
        } else if (target === 'stubbed') {
            commonTasks.unshift('stubby');
            if (watch === 'watch' || watch === 'true') {
                commonTasks.push('watch');
            }
        } else {
            commonTasks.push('open');
            commonTasks.push('watch');
        }
        grunt.task.run(commonTasks);
    });

    grunt.registerTask('test', function(type, file) {
        var protractorFile = file ? ':' + file : '';

        // define types of tests to run
        var types = {
            'unit': 'karma:single',
            'dev': 'karma:dev',
            'mid': ['server:stubbed', 'shell:protractor' + protractorFile]
        };


        // set default to run unit and func test a single time
        var tasks = [types.unit].concat(types.mid);

        // check if param passed in (e.g. 'grunt test:unit')
        if (typeof type === 'string') {
            // overwrite default tasks with single task
            tasks = types[type];
        }

        grunt.task.run(tasks);
    });

    grunt.registerTask('build', [
        'clean:dist',
        'ngdocs',
        'jshint',
        'useminPrepare',
        'concurrent:dist',
        'concat',
        'copy',
        'cdnify',
        'ngmin',
        'cssmin',
        'uglify',
        'rev',
        'usemin'
    ]);

    grunt.registerTask('docs', [
        'plato',
        'ngdocs',
        'styleguide'
    ]);

    grunt.registerTask('default', [
        'jshint',
        'karma:full',
        'simplemocha',
        'build',
        'docs'
    ]);
};
