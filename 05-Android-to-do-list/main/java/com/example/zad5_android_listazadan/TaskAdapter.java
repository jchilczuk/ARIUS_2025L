package com.example.zad5_android_listazadan;

import android.content.Context;
import android.view.*;
import android.widget.*;

import androidx.annotation.NonNull;

import java.util.List;

// TaskAdapter class is a custom ArrayAdapter used to populate a ListView with Task objects
public class TaskAdapter extends ArrayAdapter<Task> {

    // Constructor that receives context and list of tasks
    public TaskAdapter(Context context, List<Task> tasks) {
        super(context, 0, tasks); // 0 means no predefined layout ID because we use a custom one
    }

    // Returns a view for each item in the list
    @NonNull
    @Override
    public View getView(int position, View convertView, @NonNull ViewGroup parent) {
        // Get the task for the current position
        Task task = getItem(position);

        // Inflate a new view if this one is not recycled
        if (convertView == null) {
            convertView = LayoutInflater.from(getContext()).inflate(R.layout.single_row, parent, false);
        }

        // Get references to the views inside the layout
        TextView title = convertView.findViewById(R.id.taskTitle);
        TextView deadline = convertView.findViewById(R.id.taskDeadline);
        ImageView icon = convertView.findViewById(R.id.taskIcon);

        // Ensure task is not null before accessing its properties
        assert task != null;
        title.setText(task.getTitle());          // Set task title
        deadline.setText(task.getDeadline());    // Set task deadline

        // Set the appropriate icon based on task status
        if (task.getStatus() == Task.Status.DONE) {
            icon.setImageResource(R.drawable.ic_done);          // completed
        } else if (task.getStatus() == Task.Status.OVERDUE || task.isOverdue()) {
            icon.setImageResource(R.drawable.ic_overdue);       // overdue
        } else {
            icon.setImageResource(R.drawable.ic_not_done);      // not completed
        }

        // Return the fully populated view to the ListView
        return convertView;
    }
}
