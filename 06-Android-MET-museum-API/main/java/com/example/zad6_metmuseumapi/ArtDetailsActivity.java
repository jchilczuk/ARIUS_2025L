package com.example.zad6_metmuseumapi;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import com.squareup.picasso.Picasso;

// Activity that displays detailed information about a selected artwork
public class ArtDetailsActivity extends Activity {

    @SuppressLint("SetTextI18n")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_art_details); // Set layout for detail view

        // Bind all view components to corresponding layout elements
        @SuppressLint({"MissingInflatedId", "LocalSuppress"})
        ImageView imageView = findViewById(R.id.detailImage);
        @SuppressLint({"MissingInflatedId", "LocalSuppress"})
        TextView titleText = findViewById(R.id.detailTitle);
        @SuppressLint({"MissingInflatedId", "LocalSuppress"})
        TextView artistText = findViewById(R.id.detailArtist);
        @SuppressLint({"MissingInflatedId", "LocalSuppress"})
        TextView mediumText = findViewById(R.id.detailMedium);
        @SuppressLint({"MissingInflatedId", "LocalSuppress"})
        TextView dimensionsText = findViewById(R.id.detailDimensions);
        @SuppressLint({"MissingInflatedId", "LocalSuppress"})
        TextView dateText = findViewById(R.id.detailDate);
        @SuppressLint({"MissingInflatedId", "LocalSuppress"})
        Button closeButton = findViewById(R.id.closeButton);

        // Get data passed from MainActivity via Intent
        Intent intent = getIntent();
        titleText.setText(intent.getStringExtra("title"));
        artistText.setText("Artist: " + intent.getStringExtra("artist"));
        mediumText.setText("Medium: " + intent.getStringExtra("medium"));
        dimensionsText.setText("Dimensions: " + intent.getStringExtra("dimensions"));
        dateText.setText("Date: " + intent.getStringExtra("objectDate"));

        // Load and display artwork image using Picasso
        Picasso.get()
                .load(intent.getStringExtra("image"))
                .into(imageView);

        // When the user clicks the "Close" button, return data back to MainActivity
        closeButton.setOnClickListener(v -> {
            Intent resultIntent = new Intent();
            // Compose return message with title, date, and medium
            resultIntent.putExtra("message", "Closed '"
                    + intent.getStringExtra("title") + "', "
                    + intent.getStringExtra("objectDate") + "\n"
                    + intent.getStringExtra("medium"));

            // Return result and finish activity
            setResult(RESULT_OK, resultIntent);
            finish();
        });
    }
}
