using System.Linq;
using NUnit.Framework;
using UnityEngine;

namespace FW.Core.GameConfig.Tests
{
    /// <summary>EditMode tests for <see cref="ConfigAsset"/> validation.</summary>
    public sealed class ConfigAssetTests
    {
        private const string BadSpeedError = "Move Speed must be above 0.";

        private TestConfigAsset _config;

        [SetUp]
        public void SetUp()
        {
            _config = ScriptableObject.CreateInstance<TestConfigAsset>();
        }

        [TearDown]
        public void TearDown()
        {
            Object.DestroyImmediate(_config);
        }

        [Test]
        public void ReportsNoErrors_WhenSubclassFindsNone()
        {
            Assert.That(_config.GetValidationErrors(), Is.Empty);
        }

        [Test]
        public void ReportsSubclassErrors()
        {
            _config.AddError(BadSpeedError);

            Assert.That(_config.GetValidationErrors().ToList(), Is.EqualTo(new[] { BadSpeedError }));
        }
    }
}
