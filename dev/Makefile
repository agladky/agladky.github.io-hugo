.PHONY: css clean

css: clean
	sass --no-source-map scss/main.scss ../statics/base/css/main.css
	postcss --no-map ../statics/base/css/*.css --use autoprefixer -d ../statics/base/css/

clean:
	rm -f ../statics/base/css/main.css
