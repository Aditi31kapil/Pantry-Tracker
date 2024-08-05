using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

namespace Foody.User
{
    public partial class User : System.Web.UI.MasterPage
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            if (!Request.Url.AbsoluteUri.ToString().Contains("Default.aspx"))
            {
                
            }
            else
            {
                form1.Attributes.Remove("class");

                //load the control
                Control sliderUserControl = (Control)Page.LoadControl("SliderUserControl.ascx");

                //Add the Control to the Panel
                pnlSliderUC.Controls.Add(sliderUserControl);
            }
        }
    }
}