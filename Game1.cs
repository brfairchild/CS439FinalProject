using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;
using Microsoft.Xna.Framework.Input;
using System;

namespace CS439FinalProject
{
    public class Game1 : Game
    {
        GraphicsDeviceManager graphics;
        SpriteBatch spriteBatch;

        // Background color
        Color background = new Color(30, 30, 30);

        // Player
        private Player player;

        // FPS tracking
        private double fps;
        private double elapsedTime;
        private int frameCounter;

        // Font for FPS display
        private SpriteFont font;

        public static double TotalTime; // Used by Player for double-tap detection

        public Game1()
        {
            graphics = new GraphicsDeviceManager(this);
            Content.RootDirectory = "Content";
            IsMouseVisible = true;

            graphics.PreferredBackBufferWidth = 1280;
            graphics.PreferredBackBufferHeight = 960;

            // Run at 120 FPS
            graphics.SynchronizeWithVerticalRetrace = false; // Disable VSync
            IsFixedTimeStep = true;
            TargetElapsedTime = TimeSpan.FromSeconds(1.0 / 120.0);
        }

        protected override void Initialize()
        {
            player = new Player(new Vector2(graphics.PreferredBackBufferWidth / 2f,
                                            graphics.PreferredBackBufferHeight - 50f),
                                GraphicsDevice);

            base.Initialize();
        }

        protected override void LoadContent()
        {
            spriteBatch = new SpriteBatch(GraphicsDevice);

            // Load your SpriteFont (replace "Arial" with your actual font name)
            font = Content.Load<SpriteFont>("Arial");
        }

        protected override void Update(GameTime gameTime)
        {
            if (Keyboard.GetState().IsKeyDown(Keys.Escape))
                Exit();

            // Update global time for Player
            TotalTime += gameTime.ElapsedGameTime.TotalSeconds;

            // Update player
            player.Update();

            // FPS calculation
            elapsedTime += gameTime.ElapsedGameTime.TotalSeconds;
            frameCounter++;
            if (elapsedTime >= 1.0)
            {
                fps = frameCounter / elapsedTime;
                frameCounter = 0;
                elapsedTime = 0;
            }

            base.Update(gameTime);
        }

        protected override void Draw(GameTime gameTime)
        {
            GraphicsDevice.Clear(background);

            spriteBatch.Begin();

            // Draw player (player handles drawing magic circle if Shift is pressed)
            player.Draw(spriteBatch, GraphicsDevice);

            // Draw FPS
            if (font != null)
            {
                spriteBatch.DrawString(font, $"FPS: {fps:F1}", new Vector2(10, 10), Color.White);
            }

            spriteBatch.End();

            base.Draw(gameTime);
        }
    }
}
