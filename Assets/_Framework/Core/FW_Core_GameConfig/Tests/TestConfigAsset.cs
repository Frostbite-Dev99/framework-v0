using System.Collections.Generic;

namespace FW.Core.GameConfig.Tests
{
    /// <summary>Test double that reports whatever errors a test gives it.</summary>
    internal sealed class TestConfigAsset : ConfigAsset
    {
        private readonly List<string> _errors = new List<string>();

        /// <summary>Makes <see cref="GetValidationErrors"/> report this message.</summary>
        public void AddError(string error)
        {
            _errors.Add(error);
        }

        /// <inheritdoc/>
        public override IEnumerable<string> GetValidationErrors()
        {
            return _errors;
        }
    }
}
