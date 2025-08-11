package com.example.zad6_metmuseumapi;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;

import com.squareup.picasso.Picasso;

import java.util.ArrayList;

// Custom ArrayAdapter to display Artwork items in a ListView using a custom layout
public class ArtworkAdapter extends ArrayAdapter<Artwork> {
    private final Activity context;            // Reference to the parent Activity
    private final ArrayList<Artwork> artworks; // List of artworks to display

    // Constructor: initializes context and list of artworks
    public ArtworkAdapter(Activity context, ArrayList<Artwork> artworks) {
        super(context, R.layout.single_row, artworks);
        this.context = context;
        this.artworks = artworks;
    }

    // Returns a view for each item in the ListView
    @SuppressLint({"InflateParams", "SetTextI18n"})
    @NonNull
    @Override
    public View getView(int position, View convertView, @NonNull ViewGroup parent) {
        View rowView = convertView;

        // Inflate a new row layout if necessary
        if (rowView == null) {
            LayoutInflater inflater = context.getLayoutInflater();
            rowView = inflater.inflate(R.layout.single_row, null, true);
        }

        // Bind view elements to layout components
        TextView titleAndDateText = rowView.findViewById(R.id.titleAndDateText);
        TextView mediumText = rowView.findViewById(R.id.mediumText);
        ImageView imageView = rowView.findViewById(R.id.artImage);

        // Get the current artwork item from the list
        Artwork artwork = artworks.get(position);

        // Prepare title + date combination for the top line
        String combined = artwork.title;
        if (!artwork.objectDate.isEmpty()) {
            combined += ", " + artwork.objectDate;
        }

        // Set values into layout
        titleAndDateText.setText(combined);
        mediumText.setText(artwork.medium);
        Picasso.get().load(artwork.imageUrl).into(imageView); // Load image using Picasso

        return rowView; // Return the completed row to be displayed in the ListView
    }
}
