using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;
using Microsoft.Xna.Framework.Input;
using System;

namespace CS439FinalProject
{
    public class Player
    {
        public Vector2 Position;
        public float focusSpeed = 1.5f;
        public float normalSpeed = 3.5f;
        public float Speed = 3.5f;
        public int Size = 40;
        private Color color = Color.Orange;
        private Texture2D rect;

        // Double-tap detection
        private Keys lastKey = Keys.None;
        private double lastTapTime = 0;
        private const double doubleTapThreshold = 0.25; // seconds
        private KeyboardState previousKeyboardState;

        // Magic circle reference
        private MagicCircle magicCircle;
        private bool shiftHeld = false;

        public Player(Vector2 startPosition, GraphicsDevice graphicsDevice)
        {
            Position = startPosition;

            rect = new Texture2D(graphicsDevice, 1, 1);
            rect.SetData(new[] { Color.White });

            previousKeyboardState = Keyboard.GetState();

            // Initialize magic circle under player (default 5 triangles, size 60)
            magicCircle = new MagicCircle(Position, graphicsDevice, 5, 60f);
        }

        public void Update()
        {
            KeyboardState keys = Keyboard.GetState();
            double currentTime = Game1.TotalTime;

            // Movement
            if (keys.IsKeyDown(Keys.Left))
                Position.X -= Speed;
            if (keys.IsKeyDown(Keys.Right))
                Position.X += Speed;
            if (keys.IsKeyDown(Keys.Up))
                Position.Y -= Speed;
            if (keys.IsKeyDown(Keys.Down))
                Position.Y += Speed;

            // Stay in the darn screen
            Position.X = MathHelper.Clamp(Position.X, Size / 2, 1280 - Size / 2);
            Position.Y = MathHelper.Clamp(Position.Y, Size / 2, 960 - Size / 2);

            // Teleport
            CheckDoubleTap(Keys.Left, keys, currentTime, "Left");
            CheckDoubleTap(Keys.Right, keys, currentTime, "Right");

            // Focus mode
            shiftHeld = keys.IsKeyDown(Keys.LeftShift) || keys.IsKeyDown(Keys.RightShift);
            if (shiftHeld)
            {
                magicCircle.Position = Position;
                magicCircle.Grow(0.05f);
                Speed = focusSpeed;
            }
            else
            {
                magicCircle.Shrink(0.03f);
                Speed = normalSpeed;
            }

            // Update magic circle rotation
            magicCircle.Update();

            previousKeyboardState = keys;
        }

        private void CheckDoubleTap(Keys key, KeyboardState keys, double currentTime, string direction)
        {
            bool isPressed = keys.IsKeyDown(key);
            bool wasPressed = previousKeyboardState.IsKeyDown(key);

            if (isPressed && !wasPressed)
            {
                bool atEdge = false;
                switch (direction)
                {
                    case "Left": atEdge = Position.X <= Size / 2; break;
                    case "Right": atEdge = Position.X >= 1280 - Size / 2; break;
                }

                if (!atEdge)
                {
                    lastKey = key;
                    lastTapTime = currentTime;
                    return;
                }

                // Double-tap check
                if (lastKey == key && currentTime - lastTapTime <= doubleTapThreshold)
                {
                    switch (direction)
                    {
                        case "Left": Position.X = 1280 - Size / 2; break;
                        case "Right": Position.X = Size / 2; break;
                    }
                    lastKey = Keys.None;
                }
                else
                {
                    lastKey = key;
                    lastTapTime = currentTime;
                }
            }
        }

        public void Draw(SpriteBatch spriteBatch, GraphicsDevice graphicsDevice)
        {
            // Draw magic circle under player if any scale > 0
            if (magicCircle.Scale > 0f)
            {
                magicCircle.Draw(spriteBatch);
            }

            // Draw player rectangle
            spriteBatch.Draw(rect, new Rectangle((int)(Position.X - Size / 2), (int)(Position.Y - Size / 2), Size, Size), color);
        }
    }
}
