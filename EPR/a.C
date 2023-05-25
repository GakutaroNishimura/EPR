void a()
{
  TCanvas *c = new TCanvas("c","c",600,600);
  c->cd();
  TH1F *frame = gPad->DrawFrame( 0. , 0. , 0.005 , 10. );
 
  TGraphErrors *g = new TGraphErrors("./WaveData/scope_36.csv","%lg %lg","");
  g->SetMarkerStyle( 20 );
  g->SetMarkerSize( 1.0 );
  g->Draw("PC");
}