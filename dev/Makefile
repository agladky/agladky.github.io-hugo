.PHONY: css clean

css: clean
	sass --no-source-map scss/main.scss ../static/css/main.css
	postcss --no-map ../static/css/*.css --use autoprefixer -d ../static/css/

clean:
	rm -f ../static/css/main.css
