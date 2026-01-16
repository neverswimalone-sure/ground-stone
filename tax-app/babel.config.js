module.exports = function(api) {
  api.cache(true);
  return {
    presets: ['babel-preset-expo'],
    plugins: [
      [
        'module-resolver',
        {
          root: ['./src'],
          extensions: ['.ios.js', '.android.js', '.js', '.ts', '.tsx', '.json'],
          alias: {
            '@': './src',
            '@engine': './src/engine',
            '@store': './src/store',
            '@screens': './src/screens',
            '@components': './src/components',
            '@utils': './src/utils',
          },
        },
      ],
    ],
  };
};
