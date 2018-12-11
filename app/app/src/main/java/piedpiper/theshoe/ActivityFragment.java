package piedpiper.theshoe;

import android.app.Fragment;

import android.graphics.Color;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.v4.content.ContextCompat;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import android.widget.Toast;


import com.google.android.gms.tasks.OnFailureListener;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.firebase.ml.custom.FirebaseModelDataType;
import com.google.firebase.ml.custom.FirebaseModelInputOutputOptions;
import com.google.firebase.ml.custom.FirebaseModelInputs;
import com.google.firebase.ml.custom.FirebaseModelInterpreter;
import com.google.firebase.ml.custom.FirebaseModelManager;
import com.google.firebase.ml.custom.FirebaseModelOptions;
import com.google.firebase.ml.custom.FirebaseModelOutputs;
import com.google.firebase.ml.custom.model.FirebaseCloudModelSource;
import com.jjoe64.graphview.GraphView;
import com.jjoe64.graphview.series.DataPoint;
import com.jjoe64.graphview.series.LineGraphSeries;


import java.io.IOException;
import java.io.PrintWriter;
import java.io.StringWriter;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import pl.droidsonroids.gif.GifImageView;


public class ActivityFragment extends Fragment {

    private static final String TAG = "ActivityFragment";
    private static final String FETCH_URL = "http://192.168.43.34:8000/features";
    private static final int X_LEN = 6;
    private static final String[] Y_DATA = {"Walk", "Jog", "Kick", "Jump", "Idle"};

    private GifImageView gifImageView;
    private GraphView graphView;
    private TextView textView;
    private int currentGif;
    private int mCounter;
    private float probSum[][];

    private LineGraphSeries<DataPoint> xSeries;
    private LineGraphSeries<DataPoint> ySeries;
    private LineGraphSeries<DataPoint> zSeries;

    private FirebaseModelInterpreter firebaseModelInterpreter;
    private FirebaseModelInputOutputOptions firebaseModelInputOutputOptions;


    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View rootView = inflater.inflate(R.layout.fragment_activity, container, false);
        gifImageView = (GifImageView) rootView.findViewById(R.id.gif_activity_view);
        textView = (TextView) rootView.findViewById(R.id.text_activity_view);
        graphView = (GraphView) rootView.findViewById(R.id.graph_stats);
        setUpFirebaseML();
        setUpCharts();
        FetchTask fetchTask = new FetchTask();
        fetchTask.execute();
        return rootView;
    }

    private void setUpFirebaseML() {
        // cloud setup
        FirebaseCloudModelSource cloudSource = new FirebaseCloudModelSource.Builder("activity-classifier")
                .enableModelUpdates(true)
                .build();
        FirebaseModelManager.getInstance().registerCloudModelSource(cloudSource);

        // model options
        final FirebaseModelOptions options = new FirebaseModelOptions.Builder()
                .setCloudModelName("activity-classifier")
                .build();
        try {
            firebaseModelInterpreter = FirebaseModelInterpreter.getInstance(options);
            firebaseModelInputOutputOptions =
                    new FirebaseModelInputOutputOptions.Builder()
                            .setInputFormat(0, FirebaseModelDataType.FLOAT32, new int[]{1, X_LEN})
                            .setOutputFormat(0, FirebaseModelDataType.FLOAT32, new int[]{1, Y_DATA.length})
                            .build();

        } catch (Exception e) {
            Toast.makeText(getActivity().getApplicationContext(), e.toString(), Toast.LENGTH_SHORT).show();
            Log.d(TAG, e.toString());
        }

    }

    private void setUpCharts() {
        graphView.getViewport().setScalable(true);
        graphView.getViewport().setScrollable(true);
        graphView.getViewport().setScalableY(true);
        graphView.getViewport().setScrollableY(true);
        xSeries = new LineGraphSeries<>();
        xSeries.setColor(Color.RED);
        ySeries = new LineGraphSeries<>();
        ySeries.setColor(Color.GREEN);
        zSeries = new LineGraphSeries<>();
        zSeries.setColor(Color.BLUE);
        graphView.addSeries(xSeries);
        graphView.addSeries(ySeries);
        graphView.addSeries(zSeries);
    }

    private void updateResult(FirebaseModelOutputs result) {
        float[][] output = result.getOutput(0);
        float[] probabilities = output[0];
        if (mCounter%10 == 0) {
            for(int i=0;i<probabilities.length;i++){
                probabilities[i] += probSum[0][i];
            }
            resetProbSum();
        }
        else {
            for(int i=0;i<probabilities.length;i++){
                probSum[0][i] += probabilities[i];
            }
        }
        int newGif = 4;
        String newActivity = null;
        switch (getActivityFromProbability(probabilities)) {
            case 0:
                newGif = R.drawable.walk;
                newActivity = "Walking";
                break;
            case 1:
                newGif = R.drawable.run;
                newActivity = "Running";
                break;
            case 2:
                newGif = R.drawable.kick;
                newActivity = "Kicking";
                break;
            case 3:
                newGif = R.drawable.jump;
                newActivity = "Jumping";
                break;
            case 4:
                newGif = R.drawable.idle;
                newActivity = "Idle";
                break;
        }
        if (newGif != currentGif) {
            currentGif = newGif;
            gifImageView.setImageResource(currentGif);
            textView.setText("Current activity: " + newActivity);
        }
    }

    private int getActivityFromProbability(float[] array) {
        int maxAt = 0;
        for (int i = 0; i < array.length; i++) {
            maxAt = array[i] > array[maxAt] ? i : maxAt;
        }
        return maxAt;
    }

    private void resetProbSum(){
        for(int i=0;i<probSum.length;i++){
            probSum[0][i] = (float) 0.0;
        }
    }

    public class FetchTask extends AsyncTask<String, Void, String> {

        OkHttpClient mClient = new OkHttpClient();

        String run(String url) throws IOException {
            Request request = new Request.Builder()
                    .url(url)
                    .build();
            Response response = mClient.newCall(request).execute();
            String data = response.body().string();
            return data;
        }


        @Override
        protected String doInBackground(String... strings) {
            mCounter = 0;
            probSum = new float[1][Y_DATA.length];
            while (true) {
                try {

                    String raw = run(FETCH_URL);
                    String data[] = raw.split(",");
                    int dataLength = data.length;
                    data[0] = data[0].substring(1);
                    data[dataLength-1] = data[dataLength-1].substring(0, data[dataLength-1].length()-2);

                    float input[][] = new float[1][X_LEN];

                    for (int i = 0; i < X_LEN; i++) {
                        input[0][i] = Float.parseFloat(data[i]);
                    }

                    xSeries.appendData(new DataPoint(mCounter, (double) input[0][0]), true, 100, true);
                    ySeries.appendData(new DataPoint(mCounter, (double) input[0][1]), true, 100, true);
                    zSeries.appendData(new DataPoint(mCounter, (double) input[0][2]), true, 100, true);
                    graphView.getViewport().scrollToEnd();
                    mCounter++;


                    FirebaseModelInputs inputs = new FirebaseModelInputs.Builder()
                            .add(input)  // add() as many input arrays as your model requires
                            .build();

                    firebaseModelInterpreter.run(inputs, firebaseModelInputOutputOptions)
                            .addOnSuccessListener(
                                    new OnSuccessListener<FirebaseModelOutputs>() {
                                        @Override
                                        public void onSuccess(FirebaseModelOutputs result) {
                                            updateResult(result);
                                        }
                                    })
                            .addOnFailureListener(
                                    new OnFailureListener() {
                                        @Override
                                        public void onFailure(@NonNull Exception e) {
                                            Toast.makeText(getActivity().getApplicationContext(), e.toString(), Toast.LENGTH_SHORT).show();
                                            StringWriter errors = new StringWriter();
                                            e.printStackTrace(new PrintWriter(errors));
                                            Log.d(TAG, errors.toString());
                                        }
                                    });
                    Thread.sleep(200);
                } catch (Exception e) {
                    return e.toString();
                }
            }
        }
    }

}
