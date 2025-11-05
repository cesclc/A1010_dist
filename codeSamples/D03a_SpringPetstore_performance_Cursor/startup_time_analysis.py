import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Data from the table
data = {
    'Run JDK': ['(graal)', '25-AOTc', '25', '17', '17', '25'],
    'Bld JDK': ['17', '25', '25', '17', '25', '17'],
    'SBoot ver': ['3.5.6', '4.0.0', '4.0.0', '3.5.6', '4.0.0', '3.5.6'],
    'Seconds': [0.36, 3.94, 6.54, 6.63, 6.73, 6.97]
}

# Create DataFrame
df = pd.DataFrame(data)

# Create figure with subplots
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))

# Color mapping for different configurations
colors = {
    '(graal)': '#FF6B6B',      # Red for GraalVM
    '25-AOTc': '#4ECDC4',      # Teal for AOT cache
    '25': '#45B7D1',           # Blue for JDK 25
    '17': '#96CEB4'            # Green for JDK 17
}

# 1. Bar chart by Run JDK
run_jdk_counts = df['Run JDK'].value_counts()
bars1 = ax1.bar(run_jdk_counts.index, run_jdk_counts.values, 
                color=[colors.get(x, '#95A5A6') for x in run_jdk_counts.index])
ax1.set_title('Startup Time by Run JDK', fontsize=14, fontweight='bold')
ax1.set_ylabel('Number of Tests')
ax1.set_xlabel('Run JDK Version')

# Add value labels on bars
for bar in bars1:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height + 0.05,
             f'{int(height)}', ha='center', va='bottom')

# 2. Startup time comparison (main chart)
x_pos = np.arange(len(df))
bars2 = ax2.bar(x_pos, df['Seconds'], 
                color=[colors.get(x, '#95A5A6') for x in df['Run JDK']])

ax2.set_title('Spring Boot Startup Time Comparison', fontsize=14, fontweight='bold')
ax2.set_ylabel('Startup Time (seconds)')
ax2.set_xlabel('Configuration')

# Create labels for x-axis
labels = [f"{row['Run JDK']}\n{row['Bld JDK']}\nSB {row['SBoot ver']}" 
          for _, row in df.iterrows()]
ax2.set_xticks(x_pos)
ax2.set_xticklabels(labels, rotation=45, ha='right', fontsize=10)

# Add value labels on bars
for i, (bar, seconds) in enumerate(zip(bars2, df['Seconds'])):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
             f'{seconds:.2f}s', ha='center', va='bottom', fontweight='bold')

# Add horizontal line for average
avg_time = df['Seconds'].mean()
ax2.axhline(y=avg_time, color='red', linestyle='--', alpha=0.7, 
            label=f'Average: {avg_time:.2f}s')
ax2.legend()

# 3. Performance improvement chart
# Calculate improvement over baseline (JDK 17, SB 3.5.6)
baseline_time = df[(df['Run JDK'] == '17') & (df['SBoot ver'] == '3.5.6')]['Seconds'].iloc[0]
improvements = ((baseline_time - df['Seconds']) / baseline_time * 100)

bars3 = ax3.bar(x_pos, improvements, 
                color=['green' if x > 0 else 'red' for x in improvements])
ax3.set_title('Performance Improvement vs Baseline\n(JDK 17, Spring Boot 3.5.6)', 
              fontsize=14, fontweight='bold')
ax3.set_ylabel('Improvement (%)')
ax3.set_xlabel('Configuration')
ax3.set_xticks(x_pos)
ax3.set_xticklabels(labels, rotation=45, ha='right', fontsize=10)

# Add value labels on bars
for i, (bar, improvement) in enumerate(zip(bars3, improvements)):
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., 
             height + (2 if height > 0 else -3),
             f'{improvement:.1f}%', ha='center', 
             va='bottom' if height > 0 else 'top', fontweight='bold')

# Add horizontal line at 0%
ax3.axhline(y=0, color='black', linestyle='-', alpha=0.3)

# Adjust layout
plt.tight_layout()

# Add overall title
fig.suptitle('Spring Boot Application Startup Time Analysis', 
             fontsize=16, fontweight='bold', y=1.02)

# Create legend for colors
legend_elements = [plt.Rectangle((0,0),1,1, facecolor=colors[key], label=key) 
                   for key in colors.keys()]
fig.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.98, 0.98))

# Save the plot
plt.savefig('startup_time_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

# Print summary statistics
print("\n" + "="*60)
print("STARTUP TIME ANALYSIS SUMMARY")
print("="*60)
print(f"Fastest startup: {df.loc[df['Seconds'].idxmin(), 'Run JDK']} ({df['Seconds'].min():.2f}s)")
print(f"Slowest startup: {df.loc[df['Seconds'].idxmax(), 'Run JDK']} ({df['Seconds'].max():.2f}s)")
print(f"Average startup time: {df['Seconds'].mean():.2f}s")
print(f"Standard deviation: {df['Seconds'].std():.2f}s")

print("\nPerformance vs Baseline (JDK 17, SB 3.5.6):")
for _, row in df.iterrows():
    improvement = ((baseline_time - row['Seconds']) / baseline_time * 100)
    print(f"{row['Run JDK']} (SB {row['SBoot ver']}): {improvement:+.1f}% ({row['Seconds']:.2f}s)")

print("\nKey Insights:")
print(f"• GraalVM native image is {baseline_time/df['Seconds'].min():.1f}x faster than baseline")
print(f"• JDK 25 with AOT cache is {baseline_time/df[df['Run JDK']=='25-AOTc']['Seconds'].iloc[0]:.1f}x faster than baseline")
print(f"• JDK 25 standard is {improvement:.1f}% slower than baseline")
