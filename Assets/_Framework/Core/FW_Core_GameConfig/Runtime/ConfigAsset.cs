using System.Collections.Generic;
using UnityEngine;

namespace FW.Core.GameConfig
{
    /// <summary>
    /// Base class for every settings asset (global variables stored as a file instead of a static).
    /// Inherit from it, add <c>[SerializeField] private</c> fields with read-only properties,
    /// and add <c>[CreateAssetMenu]</c> so the asset can be created from the Project window.
    /// Scripts get the asset through an Inspector reference and treat it as read-only at runtime.
    /// </summary>
    public abstract class ConfigAsset : ScriptableObject
    {
        /// <summary>
        /// Returns one message per invalid value. Override it and <c>yield return</c> a message
        /// for each bad value, e.g. <c>if (_moveSpeed &lt;= 0f) yield return "Move Speed must be above 0.";</c>
        /// The Editor logs these as warnings whenever the asset is edited.
        /// </summary>
        public virtual IEnumerable<string> GetValidationErrors()
        {
            yield break;
        }

        /// <summary>
        /// Logs validation errors when the asset changes in the Editor.
        /// If you override it, call <c>base.OnValidate()</c> to keep the warnings.
        /// </summary>
        protected virtual void OnValidate()
        {
            foreach (string error in GetValidationErrors())
            {
                Debug.LogWarning($"{name}: {error}", this);
            }
        }
    }
}
