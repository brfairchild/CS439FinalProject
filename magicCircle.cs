using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;
using System;

namespace CS439FinalProject
{
    public class MagicCircle
    {
        public Vector2 Position; // Center
        public float Scale = 0f; // 0 = hidden, 1 = full size
        private int numTriangles;
        private float triangleSize;
        private float[] angles;
        private float[] speeds;
        private Color[] colors;
        private Random random;
        private Texture2D pixel;

        private Color[] triangleColors = new Color[]
        {
            Color.Cyan,
            Color.Magenta,
            Color.Yellow,
            Color.Purple,
            Color.Orange
        };

        public MagicCircle(Vector2 position, GraphicsDevice graphicsDevice, int numTriangles = 5, float triangleSize = 50f)
        {
            Position = position;
            this.numTriangles = numTriangles;
            this.triangleSize = triangleSize;

            angles = new float[numTriangles];
            speeds = new float[numTriangles];
            colors = new Color[numTriangles];

            random = new Random();

            for (int i = 0; i < numTriangles; i++)
            {
                angles[i] = 0f;
                speeds[i] = (float)(0.01 + random.NextDouble() * 0.04);
                colors[i] = triangleColors[i % triangleColors.Length];
            }

            // Create pixel **once**
            pixel = new Texture2D(graphicsDevice, 1, 1);
            pixel.SetData(new[] { Color.White });
        }

        public void Update()
        {
            for (int i = 0; i < numTriangles; i++)
            {
                angles[i] += speeds[i];
            }
        }

        public void Draw(SpriteBatch spriteBatch)
        {
            for (int i = 0; i < numTriangles; i++)
            {
                DrawTriangle(spriteBatch, pixel, Position, triangleSize * Scale, angles[i], colors[i]);
            }
        }

        private void DrawTriangle(SpriteBatch spriteBatch, Texture2D pixel, Vector2 center, float size, float rotation, Color color)
        {
            Vector2 p1 = new Vector2(0, -size);
            Vector2 p2 = new Vector2(-size * (float)Math.Sin(Math.PI / 3), size / 2);
            Vector2 p3 = new Vector2(size * (float)Math.Sin(Math.PI / 3), size / 2);

            p1 = RotatePoint(p1, rotation) + center;
            p2 = RotatePoint(p2, rotation) + center;
            p3 = RotatePoint(p3, rotation) + center;

            DrawLine(spriteBatch, pixel, p1, p2, color, 2);
            DrawLine(spriteBatch, pixel, p2, p3, color, 2);
            DrawLine(spriteBatch, pixel, p3, p1, color, 2);
        }

        private Vector2 RotatePoint(Vector2 point, float angle)
        {
            float cos = (float)Math.Cos(angle);
            float sin = (float)Math.Sin(angle);
            return new Vector2(point.X * cos - point.Y * sin, point.X * sin + point.Y * cos);
        }

        private void DrawLine(SpriteBatch spriteBatch, Texture2D pixel, Vector2 start, Vector2 end, Color color, int thickness)
        {
            Vector2 edge = end - start;
            float angle = (float)Math.Atan2(edge.Y, edge.X);
            spriteBatch.Draw(pixel, start, null, color,
                             angle, Vector2.Zero, new Vector2(edge.Length(), thickness),
                             SpriteEffects.None, 0);
        }

        // Call to grow smoothly
        public void Grow(float amount)
        {
            Scale += amount;
            Scale = MathHelper.Clamp(Scale, 0f, 1f);
        }

        // Call to shrink smoothly
        public void Shrink(float amount)
        {
            Scale -= amount;
            Scale = MathHelper.Clamp(Scale, 0f, 1f);
        }
    }
}
