package piedpiper.theshoe;

import android.app.Fragment;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.Toast;

import com.jaredrummler.materialspinner.MaterialSpinner;


public class TrainFragment extends Fragment {

    private static final String[] OPTIONS = {"Walk", "Jog", "Kick", "Jump", "Idle"};

    private Button spinnerButton;
    private MaterialSpinner spinner;

    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container, Bundle savedInstanceState) {
        View rootView = inflater.inflate(R.layout.fragment_train, container, false);
        spinner = (MaterialSpinner) rootView.findViewById(R.id.spinner);
        spinner.setItems(OPTIONS);
        spinnerButton = (Button) rootView.findViewById(R.id.spinner_button);
        spinnerButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Toast.makeText(getContext(), OPTIONS[spinner.getSelectedIndex()], Toast.LENGTH_SHORT).show();
            }
        });
        return rootView;
    }
}