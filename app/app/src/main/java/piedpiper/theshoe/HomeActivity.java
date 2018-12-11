package piedpiper.theshoe;

import android.app.Fragment;
import android.app.FragmentTransaction;
import android.content.Context;
import android.support.annotation.NonNull;
import android.support.design.widget.BottomNavigationView;
import android.support.v7.app.ActionBar;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;


public class HomeActivity extends AppCompatActivity {

    ActionBar mActionBar;
    BottomNavigationView mBottomNavigationView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_home);
        setUpActionBar();
        setUpBottomNavigation();
    }

    private void setUpActionBar() {
        mActionBar = getSupportActionBar();
        if (mActionBar != null) {
            mActionBar.setDisplayShowCustomEnabled(true);
            mActionBar.setDisplayShowTitleEnabled(false);
        }
        // inflate layout
        LayoutInflater inflator = (LayoutInflater) this
                .getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        View v = inflator.inflate(R.layout.action_bar, null);
        mActionBar.setCustomView(v);
    }

    private void setUpBottomNavigation() {
        mBottomNavigationView = (BottomNavigationView) findViewById(R.id.bottom_navigation);
        setDefaultOption();
        mBottomNavigationView.setOnNavigationItemSelectedListener(new BottomNavigationView.OnNavigationItemSelectedListener() {
            @Override
            public boolean onNavigationItemSelected(@NonNull MenuItem item) {
                selectBottomFragment(item);
                return true;
            }
        });
    }

    private void setDefaultOption() {
        Menu bottomMenu = mBottomNavigationView.getMenu();
        MenuItem defaultItem = bottomMenu.getItem(0);
        selectBottomFragment(defaultItem);
        defaultItem.setChecked(true);
    }

    private void selectBottomFragment(MenuItem item) {
        Fragment fragment = null;
        switch (item.getItemId()) {
            case R.id.menu_item_activity:
                fragment = new ActivityFragment();
                break;
            case R.id.menu_item_train:
                fragment = new TrainFragment();
                break;
            case R.id.menu_item_profile:
                fragment = new ProfileFragment();
                break;
        }

        if (fragment != null) {
            FragmentTransaction fragmentTransaction = getFragmentManager().beginTransaction();
            fragmentTransaction.replace(R.id.container, fragment);
            fragmentTransaction.addToBackStack(null);
            fragmentTransaction.commitAllowingStateLoss();
        }
    }
}
