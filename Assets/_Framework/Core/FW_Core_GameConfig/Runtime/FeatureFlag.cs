using UnityEngine;

namespace FW.Core.GameConfig
{
    /// <summary>
    /// An on/off switch saved as an asset, one asset per feature.
    /// Create one with Create > FW > GameConfig > Feature Flag, then drag it into a script's
    /// <c>[SerializeField] private FeatureFlag</c> field and check <see cref="IsEnabled"/>.
    /// </summary>
    [CreateAssetMenu(menuName = "FW/GameConfig/Feature Flag", fileName = "NewFeatureFlag")]
    public sealed class FeatureFlag : ConfigAsset
    {
        [SerializeField, Tooltip("Whether the feature is on.")]
        private bool _isEnabled;

        [SerializeField, TextArea, Tooltip("What this flag turns on, so teammates know what they are switching.")]
        private string _description;

        /// <summary>True when the feature is on. Read-only at runtime.</summary>
        public bool IsEnabled => _isEnabled;

        /// <summary>What this flag turns on.</summary>
        public string Description => _description;
    }
}
