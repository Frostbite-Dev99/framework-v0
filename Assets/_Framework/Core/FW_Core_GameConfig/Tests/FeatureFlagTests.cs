using NUnit.Framework;
using UnityEngine;

namespace FW.Core.GameConfig.Tests
{
    /// <summary>EditMode tests for <see cref="FeatureFlag"/>.</summary>
    public sealed class FeatureFlagTests
    {
        private FeatureFlag _flag;

        [SetUp]
        public void SetUp()
        {
            _flag = ScriptableObject.CreateInstance<FeatureFlag>();
        }

        [TearDown]
        public void TearDown()
        {
            Object.DestroyImmediate(_flag);
        }

        [Test]
        public void NewFlag_IsOff()
        {
            Assert.That(_flag.IsEnabled, Is.False);
        }

        [Test]
        public void NewFlag_HasNoValidationErrors()
        {
            Assert.That(_flag.GetValidationErrors(), Is.Empty);
        }
    }
}
